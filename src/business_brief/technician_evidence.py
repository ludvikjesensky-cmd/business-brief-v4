"""Mechanical page evidence and text-layer checks; no article interpretation."""
from __future__ import annotations

import hashlib
import math
import platform
import re
import shutil
import subprocess
from pathlib import Path

import pymupdf as fitz

from .contracts import PageImage, PageTextCheck, PreviewImage


def file_sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def tool_versions(ocr_binary: str) -> dict[str, str | None]:
    result = {"python": platform.python_version(), "pymupdf": fitz.VersionBind}
    for name, binary in (("ocrmypdf", ocr_binary), ("tesseract", "tesseract"), ("ghostscript", "gs")):
        executable = shutil.which(binary)
        result[name] = None
        if executable:
            try:
                run = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=10)
                lines = (run.stdout or run.stderr).strip().splitlines()
                if run.returncode == 0 and lines:
                    result[name] = lines[0]
            except (OSError, subprocess.TimeoutExpired):
                pass
    return result


def embedded_image(doc, page):
    """Extract only an unrotated, full-page image with no visible overlays.

    Conservative fallback to render for crops, masks, text, drawings, widgets,
    annotations, inline images or transformed placements. No semantic detection.
    """
    if (page.rotation or page.get_text().strip() or page.get_drawings()
            or page.first_annot or page.first_widget
            or page.cropbox != page.mediabox or page.get_xobjects()):
        return None
    # A full-page image bbox alone does not prove it is fully visible: clipping
    # and graphics-state transparency can change its visible footprint.
    commands = b"\n".join(doc.xref_stream(xref) for xref in page.get_contents())
    if re.search(rb"(?<!\S)(?:W\*?|gs)(?!\S)", commands):
        return None
    images = page.get_image_info(xrefs=True)
    if len(images) != 1:
        return None
    image = images[0]
    xref = image.get("xref", 0)
    if not xref:
        return None
    if any(item[0] == xref and item[1] for item in page.get_images(full=True)):
        return None
    rect = page.rect
    bbox = image["bbox"]
    if any(abs(a - b) > 0.01 for a, b in zip(bbox, tuple(rect))):
        return None
    a, b, c, d, _, _ = image["transform"]
    if a <= 0 or d <= 0 or abs(b) > 0.01 or abs(c) > 0.01:
        return None
    extracted = doc.extract_image(xref)
    # PNG/JPEG are supported downstream; other encodings use a visible render.
    if not extracted or extracted["ext"] not in {"png", "jpeg", "jpg"}:
        return None
    return extracted


def prepare_images(src: Path, out: Path, *, dpi: int, image_mode: str,
                   preview_width: int, contact_columns: int, max_render_pixels: int):
    pages_dir = out / "pages"
    preview_dir = out / "previews"
    pages_dir.mkdir(parents=True)
    preview_dir.mkdir(parents=True)
    pages, previews = [], []
    with fitz.open(src) as doc:
        for number, page in enumerate(doc, 1):
            original = embedded_image(doc, page) if image_mode == "auto" else None
            if original:
                ext = "jpg" if original["ext"] == "jpeg" else original["ext"]
                target = pages_dir / f"page-{number:04d}.{ext}"
                target.write_bytes(original["image"])
                pix = fitz.Pixmap(original["image"])
                method = "embedded_original"
                effective_dpi = min(pix.width / page.rect.width, pix.height / page.rect.height) * 72
            else:
                scale = min(dpi / 72, math.sqrt(max_render_pixels / (page.rect.width * page.rect.height)))
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
                target = pages_dir / f"page-{number:04d}.png"
                pix.save(target)
                method = "render"
                effective_dpi = scale * 72
            pages.append(PageImage(number, str(target), pix.width, pix.height,
                                   file_sha(target), method, round(effective_dpi, 3)))
            if pix.colorspace and pix.colorspace.n != 3:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            scale = min(1.0, preview_width / pix.width)
            thumb = fitz.Pixmap(pix, max(1, round(pix.width * scale)), max(1, round(pix.height * scale)))
            if thumb.alpha:
                thumb = fitz.Pixmap(thumb, 0)
            preview = preview_dir / f"page-{number:04d}.jpg"
            thumb.save(preview, jpg_quality=80)
            previews.append(PreviewImage(str(preview), thumb.width, thumb.height, file_sha(preview), number))
    columns = min(contact_columns, len(previews))
    cell_width = preview_width + 16
    cell_height = max(p.height_px for p in previews) + 32
    rows = math.ceil(len(previews) / columns)
    with fitz.open() as sheet:
        page = sheet.new_page(width=columns * cell_width, height=rows * cell_height)
        for i, preview in enumerate(previews):
            x, y = (i % columns) * cell_width + 8, (i // columns) * cell_height + 24
            page.insert_text((x, y - 8), f"PDF page {preview.page_no}", fontsize=10)
            page.insert_image(fitz.Rect(x, y, x + preview.width_px, y + preview.height_px), filename=preview.path)
        scale = min(1.0, math.sqrt(max_render_pixels / (page.rect.width * page.rect.height)))
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
        target = preview_dir / "contact-sheet.jpg"
        pix.save(target, jpg_quality=85)
        contact = PreviewImage(str(target), pix.width, pix.height, file_sha(target))
    return tuple(pages), tuple(previews), contact


def check_text_layers(original: Path, prepared: Path, native_counts, *, min_chars: int,
                      ocr_pages: tuple[int, ...]) -> tuple[PageTextCheck, ...]:
    checks = []
    with fitz.open(original) as source, fitz.open(prepared) as result:
        if len(source) != len(result):
            raise ValueError("OCR derivative page count mismatch")
        for n, (before, after) in enumerate(zip(source, result), 1):
            chars = len("".join(after.get_text().split()))
            words = after.get_text("words")
            # Extraction coordinates are unrotated, even when Page.rect is not.
            bounds = after.rect * after.derotation_matrix
            invalid = 0
            for word in words:
                x0, y0, x1, y1 = word[:4]
                if (not all(math.isfinite(v) for v in word[:4]) or x1 <= x0 or y1 <= y0
                        or x0 < bounds.x0 - 2 or y0 < bounds.y0 - 2
                        or x1 > bounds.x1 + 2 or y1 > bounds.y1 + 2):
                    invalid += 1
            # Rotation changes the original/image coordinate transform. Do not
            # silently hand an unaligned image/text pair to the Ingestor.
            geometry_ok = (before.rotation == after.rotation and
                           all(abs(a - b) <= 0.1 for a, b in zip(tuple(before.cropbox), tuple(after.cropbox))))
            if not geometry_ok or invalid:
                status = "INVALID_TEXT_GEOMETRY"
            elif native_counts[n - 1] >= min_chars and not chars:
                status = "TEXT_LAYER_LOST"
            elif chars >= min_chars:
                status = "TEXT_AVAILABLE"
            elif n in ocr_pages and not chars:
                status = "OCR_NO_TEXT_REVIEW"
            else:
                status = "LOW_TEXT_REVIEW"
            checks.append(PageTextCheck(n, native_counts[n - 1], chars, len(words), invalid,
                                       before.rect.width, before.rect.height,
                                       after.rect.width, after.rect.height, status))
    return tuple(checks)
