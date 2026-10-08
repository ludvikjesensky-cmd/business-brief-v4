# Python installation and Railway

The project uses setuptools with the `src` layout. Install the package, rather
than relying on `PYTHONPATH` to make application code visible:

```sh
uv sync --locked --extra dev
uv run --locked pytest
uv run --locked python -c 'import supabase; from supabase import create_client; print(supabase.__file__)'
uv run --locked python -m business_brief.dashboard
```

`uv.lock` pins production and development dependencies (including Supabase) and
lets Railpack detect the uv installer. `.python-version` selects Python 3.13.
Keep the lockfile committed when changing `pyproject.toml` (`uv lock`).

Dashboard start command: `python -m business_brief.dashboard` (the existing
`PYTHONPATH=src python -m business_brief.dashboard` also works). The HTTP server
listens on `0.0.0.0:$PORT`, defaulting to 8080 for local use. Runtime needs
`SUPABASE_URL` and `SUPABASE_SECRET_KEY`; keep values in Railway variables.
Check both `/` and `/api/dashboard` after deploying: HTML alone does not confirm
database access.

The top-level `supabase/` directory contains SQL migrations, not Python code.
Without the installed Supabase distribution, Python treats it as a namespace
package and `from supabase import create_client` fails with `unknown location`.
Do not rename migrations or add an `__init__.py` there to work around a missing
dependency installation.
