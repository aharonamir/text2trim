# Development Environment Record

**Checked**: 2026-10-10  
**Environment**: Ubuntu 22.04.5 on WSL2; product target remains Windows 10/11.

## Available toolchain

| Component | Observed version or state |
|---|---|
| `uv` | 0.7.2 |
| Python | 3.12.13 in the Linux project `.venv`; project supports Python 3.11+ |
| FFmpeg / FFprobe | 4.4.2, installed |
| Ollama client | 0.20.5 |
| CPU | Intel Core i5-11400F, 6 cores / 12 threads |
| RAM | 7.6 GiB visible to WSL |
| Disk | 857 GiB available at inspection |
| NVIDIA GPU | Not visible; NVML reports GPU access blocked |

`uv sync` should be run from this WSL checkout to maintain the Linux `.venv`. Never copy or reuse a Windows virtual environment here.

The default shared uv cache contains a read-only `.git` marker that prevents uv from opening it. Sync and worker startup succeeded with an isolated writable cache:

```bash
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv sync --python /usr/bin/python3.12
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv run python -m text2trim
```

No project dependency changes were needed. The checkout's `.git` directory is empty, so Git status/history commands cannot inspect this workspace.

The browser UI and Python API use only the standard library and static files; no Node packages or Windows GUI libraries are needed for this WSL development shell. The Codex command sandbox denies socket creation (`PermissionError: Operation not permitted`), so the server cannot be launched or browser/API round-tripped from this agent session. Syntax and contract JSON checks pass; launch it from a regular WSL terminal for an interactive check.

## Model benchmark availability

The Ollama model store contains `qwen3-vl:4b` (API-reported size 3,295,636,135 bytes; digest `1343d82ebee38e26a4dd6b0180b915eb91550184e67c505dea97509571c8f683`; 4.4B parameters, Q4_K_M) and `qwen3.5:9b`. The `qwen3-vl:4b` manifest includes Apache-2.0 license text. The user confirmed `/api/tags` responds in another WSL terminal, but the endpoint is not reachable from the Codex execution sandbox. No model was downloaded during this task. The current machine also cannot validate the plan's stated 8 GB NVIDIA GPU target. The first inference output was invalid because the original synthetic clip rendered as plain gray; the fixture was corrected, visually checked, and the corrected run below succeeded.

### Qwen3-VL smoke benchmark

Run `scripts/benchmark_qwen3_vl.py` from a WSL terminal that can reach Ollama. The three-frame fixture is a synthetic 4-second clip; this is a pipeline smoke check, not an accuracy benchmark.

| Run | Wall time | Model output |
|---|---:|---|
| 1 | 4.52 s | Correctly identified red square moving horizontally right; interval 250–3750 ms |
| 2 | 3.77 s | Same |
| 3 | 3.77 s | Same |

The model reported high confidence. Warm-run generation took about 3.52 s for 369 output tokens (about 105 tokens/s). This WSL host has 6 CPU cores, 7.6 GiB visible RAM, and no GPU access; peak memory was not measured. These results do not establish performance on the Windows target PC or accuracy across real-world clips.

```bash
UV_CACHE_DIR=/tmp/text2trim-uv-cache uv run python scripts/benchmark_qwen3_vl.py --host http://0.0.0.0:11434
```


This record describes the development environment only. It is not a Windows build or release verification.
