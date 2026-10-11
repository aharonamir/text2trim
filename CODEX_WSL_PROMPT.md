# Prompt for Codex in WSL

You are continuing development of **Text2Trim**, a local-first video editing app. The repository contains its current product spec, technical plan, ordered task list, and a minimal Python package. Read `README.md` and all files under `specs/001-natural-language-trimming/` before changing code. Follow any `AGENTS.md` instructions present in the checkout.

## Product goal

Build a simple desktop app where a user selects a local video, describes in chat what to keep or cut using speech and visible scene/action descriptions, reviews evidence-backed candidate ranges, sees job progress, and exports a playable result. Media processing and inference should run locally. The selected product target remains Windows desktop; this checkout and development environment are WSL/Linux.

## How to work

1. Treat `spec.md` as the product requirements, `plan.md` as the proposed design, and `tasks.md` as the implementation order. If they conflict, explain the conflict and update the documents before coding.
2. Use `uv` for all Python environment and dependency work. Create a Linux virtual environment in this checkout with `uv sync`; never reuse a Windows `.venv`.
3. Start with the feasibility spike and a minimal runnable worker. Check installed tools (`uv`, Python, FFmpeg/FFprobe, GPU visibility) and report unavailable dependencies. Do not download large models without explaining their sizes and licenses in the project docs.
4. Keep media paths local. Do not add cloud inference or upload behavior. Invoke external programs with argument arrays, never shell-interpolated user text.
5. Implement in small increments, keep `tasks.md` current, and run focused checks for each completed behavior. Report commands and outcomes. Do not claim unimplemented features work.
6. Keep Windows packaging constraints visible: validate the worker and media pipeline in WSL first, but do not claim a Windows installer is produced unless it is built and verified on a suitable Windows toolchain.

## First objective

Inspect the checkout and local toolchain, then complete the first useful slice of Phase 1: document the environment, establish a small licensed fixture/evaluation format, and benchmark the proposed local vision candidate `qwen3-vl:4b` only if it is already installed or can be acquired within the available network/storage constraints. Also verify the Python worker starts with `uv run python -m text2trim`. Update `tasks.md` with truthful progress and recommend the next implementation task. Do not attempt to build the entire app in one turn.
