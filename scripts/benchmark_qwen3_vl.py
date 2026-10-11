"""Run a small local visual-motion smoke benchmark against Ollama."""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen3-vl:4b"
FIXTURE = ROOT / "tests/fixtures/media/synthetic-red-motion.mp4"
FRAME_TIMES = (0.25, 2.0, 3.75)


def request_json(url: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if data is not None else {},
    )
    try:
        with urlopen(request, timeout=600) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Ollama request failed at {url}: {exc}") from exc


def extract_frames(ffmpeg: str, directory: Path) -> list[str]:
    encoded_frames = []
    for index, timestamp in enumerate(FRAME_TIMES):
        frame_path = directory / f"frame-{index}.jpg"
        command = [
            ffmpeg,
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            str(timestamp),
            "-i",
            str(FIXTURE),
            "-frames:v",
            "1",
            "-q:v",
            "3",
            str(frame_path),
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        encoded_frames.append(base64.b64encode(frame_path.read_bytes()).decode("ascii"))
    return encoded_frames


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host",
        default=os.environ.get("OLLAMA_HOST", "http://0.0.0.0:11434"),
        help="Ollama base URL (default: OLLAMA_HOST or http://0.0.0.0:11434)",
    )
    parser.add_argument("--ffmpeg", default="ffmpeg", help="FFmpeg executable")
    parser.add_argument("--repeat", type=int, default=3, help="Inference runs (default: 3)")
    args = parser.parse_args()
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")

    host = args.host.rstrip("/")
    tags = request_json(f"{host}/api/tags")
    model = next((item for item in tags.get("models", []) if item.get("name") == MODEL), None)
    if model is None:
        raise RuntimeError(f"{MODEL} is not listed by {host}/api/tags")

    prompt = (
        "These are three frames in chronological order from a 4-second silent video, "
        "sampled at 0.25s, 2.0s, and 3.75s. Describe only visible evidence. "
        "Does a red square move horizontally across a gray background? If so, give "
        "the direction and an approximate source-time interval. Return concise JSON "
        "with keys: object, motion, start_ms, end_ms, confidence."
    )
    result: dict[str, Any] = {
        "model": model,
        "fixture": str(FIXTURE.relative_to(ROOT)),
        "frame_times_seconds": FRAME_TIMES,
        "runs": [],
    }

    with tempfile.TemporaryDirectory(prefix="text2trim-qwen-benchmark-") as temp_dir:
        images = extract_frames(args.ffmpeg, Path(temp_dir))
        for run_number in range(1, args.repeat + 1):
            started = time.perf_counter()
            response = request_json(
                f"{host}/api/chat",
                {
                    "model": MODEL,
                    "stream": False,
                    "options": {"temperature": 0},
                    "messages": [{"role": "user", "content": prompt, "images": images}],
                },
            )
            wall_ms = round((time.perf_counter() - started) * 1000, 1)
            result["runs"].append(
                {
                    "run": run_number,
                    "wall_ms": wall_ms,
                    "total_duration_ns": response.get("total_duration"),
                    "load_duration_ns": response.get("load_duration"),
                    "prompt_eval_count": response.get("prompt_eval_count"),
                    "prompt_eval_duration_ns": response.get("prompt_eval_duration"),
                    "eval_count": response.get("eval_count"),
                    "eval_duration_ns": response.get("eval_duration"),
                    "response": response.get("message", {}).get("content"),
                }
            )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(str(exc)) from exc
