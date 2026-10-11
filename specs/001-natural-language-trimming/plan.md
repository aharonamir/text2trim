# Implementation Plan: Natural-language video trimming

**Input**: [spec.md](spec.md)  
**Target**: Windows desktop; local processing  
**Status**: Proposed architecture; validate model performance in a spike before locking model choices

## Technical context

For WSL development, serve a browser UI built with HTML, CSS, and JavaScript from the local Python worker. Expose a versioned JSON API on loopback for UI/worker communication. The UI owns file selection, chat, timeline, preview, progress, and export controls. The worker owns media probing, indexing, grounded matching, and FFmpeg jobs. Use local model runners, not remote APIs. Keep model adapters replaceable so the first model choice can be changed after hardware and accuracy testing. The product target remains Windows desktop; a native Windows wrapper can be added after the browser workflow is proven.

| Concern | Proposed component | Reason |
|---|---|---|
| WSL development UI | Browser-served HTML/CSS/JavaScript | Runs inside WSL without a Windows desktop toolchain and talks to the local worker over versioned JSON |
| Windows product shell | Deferred native wrapper | Preserve the Windows 10/11 product target; choose packaging after the browser workflow and IPC contract stabilize |
| Media inspection/editing | FFprobe + FFmpeg | Reliable stream metadata, frame extraction, trim/concat, encoding, and machine-readable progress |
| Speech index | whisper.cpp or equivalent local ASR | Timestamped speech without cloud processing |
| Visual index | PySceneDetect + FFmpeg frame sampling + OpenCLIP image/text embeddings | Find shot boundaries, then retrieve shots matching objects and scene descriptions; sample more densely around likely matches |
| Action verification | Local vision-language model over short frame sequences | Verify temporal claims that single-frame similarity cannot establish |
| Instruction parsing | Local LLM with schema-constrained response | Converts user language to an intent and evidence-based candidate selection |
| Persistence | SQLite/project directory | Indexed evidence and revisions survive app restarts |

For the stated NVIDIA GPU with at least 8 GB VRAM, start the vision benchmark with `qwen3-vl:4b` through local Ollama. Compare `qwen3-vl:8b` only when available VRAM and latency permit; a model's download size is not its full runtime memory requirement. The exact ASR, embedding, and vision-language model weights remain a benchmark decision, not an architectural dependency. Package the worker and FFmpeg with the app; provide a guided first-run model setup with size, storage, and offline status. Verify licenses and distribution terms of each selected binary and model before shipping.

## Processing flow

1. **Import**: File picker or drop → normalize path → FFprobe validation → create project and fingerprint. Do not copy a large source by default.
2. **Index**: Extract analysis audio and low-resolution frames locally. Transcribe audio with timecodes; detect shot boundaries; embed representative frames; optionally caption short sequences. Store evidence with original source timestamps.
3. **Interpret request**: Parse into structured `{operation, target, constraints}`. Retrieve transcript and visual candidates, then use the local LLM/VLM to rerank and explain only retrieved evidence. Validate JSON and clamp times to media duration.
4. **Compose edit**: Maintain canonical sorted keep intervals in source time. Keep selects matching intervals; remove subtracts intervals. Apply explicit user revisions deterministically, preserving history.
5. **Review**: Display candidates on the source timeline, evidence, confidence, and result preview. Let the user adjust boundaries and resolve ambiguity.
6. **Export**: Convert the approved interval list to an FFmpeg filter graph or equivalent accurate trim/concat path. Reencode where frame-accurate cuts require it, report progress, verify output duration/playability, then finalize destination.

## Data contracts

- `Evidence`: `id`, `kind` (`speech|frame|scene|action`), `start_ms`, `end_ms`, `text`, `source_refs`, `model_id`.
- `Instruction`: `id`, `text`, `operation` (`keep|remove|modify|clarify`), `constraints`, `created_at`.
- `Candidate`: `start_ms`, `end_ms`, `evidence_ids[]`, `reason`, `score`, `needs_review`.
- `EditRevision`: `keep_intervals[]`, `parent_revision`, `instruction_id`, `manual_adjustments[]`.
- `JobEvent`: `stage`, `state`, `completed`, `total`, `message`, `error_code`.

Model output is a proposal, never an executable command. A validator checks schema, evidence IDs, interval bounds, ordering, and conflict rules before any edit changes. User-authored text and media metadata are untrusted data.

## Project structure

```text
web/                       # Browser UI served by the local Python worker
src/text2trim/             # Worker server, API, and later media/indexing modules
contracts/                 # Versioned UI/worker JSON contract
worker/models/             # Local model adapters
worker/export/             # FFmpeg graph builder and output validation
tests/fixtures/             # Small licensed video fixtures and expected events
specs/001-natural-language-trimming/
```

## Architectural decisions and risks

- **Grounding**: The LLM sees retrieved evidence with timecodes; it cannot invent an interval without an evidence ID. The UI still shows uncertainty because retrieval can be wrong.
- **Visual actions**: Frame embeddings alone cannot prove motion or ordering. Use a local vision-language verification pass on short sequences and benchmark actions separately.
- **Accuracy**: Stream-copy cuts may land on keyframes. The default export path uses accurate decode/trim and encode; a faster approximate mode can be added later.
- **Performance**: Index progressively and cache by source fingerprint plus model version. Show stage-specific progress. Define CPU and GPU expectations from the benchmark spike.
- **Security/privacy**: Bind the development API to loopback by default. Restrict worker commands to typed operations and selected paths; use argument arrays rather than shell strings. Keep inference endpoints private, and expose no remote upload path.
- **Preview**: Build a lightweight proxy or segment playlist for the edit preview, distinct from final export quality. UI should always identify whether it is showing source, proposal, or final output.

## Validation gates

1. **Feasibility spike**: Test at least 20 clips across speech, silent scenes, objects, and simple actions on the minimum target PC; record accuracy, RAM/VRAM, index time, and model size. Select model weights only after this result.
2. **MVP interaction**: Complete file selection, indexing, one keep/remove request, candidate review, manual correction, progress, cancel, export, and result playback without a terminal.
3. **Correctness**: Automated interval algebra tests and FFmpeg fixture tests for boundary accuracy, A/V sync, multi-segment output, rotation, and variable frame rate. Manual offline and clean-install checks.
4. **Release**: Verify model/binary licenses, code signing, installer size, update behavior, disk-space handling, and no outbound media traffic.

## External references

- [GitHub Spec Kit workflow](https://github.com/github/spec-kit/blob/main/docs/index.md)
- [Tauri file dialogs](https://tauri.app/plugin/dialog/) and [sidecars](https://v2.tauri.app/develop/sidecar/)
- [FFmpeg progress](https://ffmpeg.org/ffmpeg.html) and [trim filters](https://ffmpeg.org/ffmpeg-filters.html)
- [whisper.cpp](https://github.com/ggml-org/whisper.cpp)
- [OpenCLIP](https://github.com/mlfoundations/open_clip)
- [llama.cpp schema-constrained output](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
