# Text2Trim

Text2Trim is a planned Windows desktop app for trimming local videos with natural-language instructions. The user describes what to keep or remove, reviews evidence-backed candidate ranges, and exports the result. Speech transcription and visual scene/action matching are intended to run locally.

## Project status

**Current stage: Phase 1 — setup and feasibility.** The browser-based WSL shell can select and preview a local video, display readable metadata, and report local worker health. Preview errors have a recovery message, and the interface clearly labels the unavailable processing workflow. The initial Git repository is pushed to `origin/master`.

The evaluation manifest format and one synthetic CC0 fixture are ready. `qwen3-vl:4b` passed a three-run visual-motion smoke test, but the licensed 20-clip evaluation and representative Windows hardware benchmarks are still outstanding. Media indexing, chat matching, evidence review, job progress, export, and the native Windows wrapper are not implemented. Windows remains the product target; no Windows build has been produced or verified.

**Next recommended task:** complete T002 by assembling and labeling the 20-clip licensed evaluation set. See [tasks.md](specs/001-natural-language-trimming/tasks.md) for the phase checklist and dependencies.

## Run the local development app

Use Python 3.11+ and [uv](https://docs.astral.sh/uv/):

```bash
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv sync
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv run python -m text2trim
```

Open `http://127.0.0.1:8765` in a browser, then stop the server with Ctrl+C. The UI can select and preview a local file in the browser; processing actions are not connected yet. The worker serves `/api/v1/health` according to the contract in `contracts/`. The server binds to loopback only. Run these commands in the WSL/Linux checkout; `uv sync` creates or updates its Linux `.venv`. Do not copy a Windows virtual environment into this checkout. This browser shell is the WSL development interface; Windows remains the product target.

## Planning documents

- `specs/001-natural-language-trimming/spec.md` — user needs and acceptance criteria
- `specs/001-natural-language-trimming/plan.md` — architecture and validation plan
- `specs/001-natural-language-trimming/tasks.md` — implementation sequence
- `specs/001-natural-language-trimming/environment.md` — current WSL toolchain and benchmark constraints
- `tests/fixtures/README.md` — licensed fixture and evaluation case format
- `contracts/README.md` — versioned browser/worker API contract
