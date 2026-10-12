"""Opt-in Responses API adapter. One attempt, no implicit retry or Fast Editorial."""
from __future__ import annotations

import base64
import json
import os
from urllib import error, request

from .visual_page_map import LAYOUT_SCHEMA, PROMPT, PageMapError, validate_layout


def parse_response(raw, page_no):
    if raw.get("status") != "completed":
        raise PageMapError("vision response incomplete/failed; not accepted")
    content = [c for output in raw.get("output", []) for c in output.get("content", [])]
    if any(c.get("type") == "refusal" for c in content):
        raise PageMapError("vision response refused; not accepted")
    texts = [c["text"] for c in content if c.get("type") == "output_text"]
    if len(texts) != 1:
        raise PageMapError("vision response must contain exactly one layout")
    try:
        layout = json.loads(texts[0])
    except (ValueError, TypeError):
        raise PageMapError("vision response is not JSON") from None
    return validate_layout(layout, page_no)


class VisualResponsesProvider:
    def __init__(self, model, *, allow_paid=False, key=None, max_output_tokens=6000,
                 detail="low", timeout=120, transport=None):
        if not allow_paid:
            raise PageMapError("live mapping requires explicit --allow-paid")
        self.key = key or os.environ.get("OPENAI_API_KEY")
        if not model or not self.key:
            raise PageMapError("explicit vision model and OPENAI_API_KEY are required")
        if detail not in ("low", "high", "auto") or not 256 <= max_output_tokens <= 32000:
            raise PageMapError("invalid vision request limits")
        self.model, self.max_output_tokens, self.detail = model, max_output_tokens, detail
        self.timeout, self.transport = timeout, transport or request.urlopen

    def generate(self, image, metadata):
        # Metadata only. Physical Map text is never sent to the model.
        body = {"model": self.model, "store": False, "instructions": PROMPT,
            "max_output_tokens": self.max_output_tokens,
            "input": [{"role": "user", "content": [
                {"type": "input_text", "text": json.dumps(metadata, ensure_ascii=False)},
                {"type": "input_image", "detail": self.detail,
                 "image_url": "data:image/jpeg;base64," + base64.b64encode(image).decode("ascii")}]}],
            "text": {"format": {"type": "json_schema", "name": "visual_page_layout",
                                "strict": True, "schema": LAYOUT_SCHEMA}}}
        req = request.Request("https://api.openai.com/v1/responses", data=json.dumps(body).encode(),
            headers={"Authorization": "Bearer " + self.key, "Content-Type": "application/json"})
        try:
            with self.transport(req, timeout=self.timeout) as response:
                return json.load(response)
        except error.HTTPError as exc:
            # Never print API bodies or headers (may contain sensitive data).
            raise PageMapError(f"vision HTTP {exc.code}; no automatic retry") from None
        except (OSError, ValueError):
            raise PageMapError("vision transport failed; billing status may be unknown; no automatic retry") from None
