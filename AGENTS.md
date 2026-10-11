# Repository Guidelines

## Project Structure & Module Organization

`src/text2trim/` contains the Python worker and loopback HTTP server. `web/` contains the browser-based WSL development UI, and `contracts/` defines the versioned JSON API. Product requirements and architecture live in `specs/001-natural-language-trimming/`. Media processing, inference adapters, and the native Windows wrapper are not implemented yet; follow `plan.md` as work begins.

## Build, Test, and Development Commands

Use Python 3.11+ and `uv` from the WSL/Linux checkout:

```bash
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv sync
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv run python -m text2trim  # Start UI/API at 127.0.0.1:8765
```

Keep the project `.venv` Linux-native; do not copy a Windows environment into the checkout.

No frontend build step or test suite is configured; the browser shell uses plain HTML/CSS/JavaScript. Keep UI and worker calls on the versioned loopback API. When adding dependencies or checks, update `pyproject.toml` and this guide.

## Coding Style & Naming Conventions

Follow standard Python formatting with four-space indentation, type annotations for public interfaces, and concise docstrings where behavior is non-obvious. Use `snake_case` for modules, functions, and variables; `PascalCase` for classes; and `UPPER_SNAKE_CASE` for constants. Keep worker operations typed and separate from media/model adapters. Avoid shell-string construction for FFmpeg or other external commands; pass argument arrays and validate user-controlled paths.

## Testing Guidelines

Tests are not present yet. Add tests under `tests/`, mirroring the source package, with `test_*.py` files and focused names such as `test_interval_algebra.py`. Prioritize interval/revision logic, schema validation, evidence grounding, FFmpeg boundary behavior, cancellation, and source-file preservation. Add small licensed fixtures under `tests/fixtures/` and document any required media tools.

## Commit & Pull Request Guidelines

Git history is not available in this checkout, so no existing commit convention can be inferred. Use short imperative subjects (for example, `Add interval algebra`) and keep each commit focused. Pull requests should explain the behavior changed, link the relevant task or spec section, include tests or manual verification, and attach screenshots or sample output for UI/media changes. Update the relevant planning documents when implementation changes the proposed architecture.

## Security & Configuration Tips

Processing is intended to remain local. Do not upload media, transcripts, prompts, or frames. Treat user text and media metadata as untrusted; validate model output, constrain file access to selected paths, and never allow prompt content to become executable commands.
