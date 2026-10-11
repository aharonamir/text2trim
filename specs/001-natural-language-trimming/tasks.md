# Tasks: Natural-language video trimming

Tasks are ordered by dependency. The first release includes both speech and visual matching. Each user story can be demonstrated independently after the shared foundation.

## Phase 1: Setup and feasibility

- [x] T001 Create a browser-served HTML/CSS/JavaScript development shell and local Python worker skeleton with a versioned loopback JSON API. Static checks pass; live server startup must be checked in a regular WSL terminal because the Codex sandbox denies socket creation. The native Windows wrapper remains deferred until the browser workflow is proven.
- [ ] T002 Assemble 20 short, licensed evaluation clips and label speech, scene, object, action, and desired cut boundaries. Evaluation manifest format and one synthetic CC0 fixture are established; the 20-clip corpus remains pending.
- [ ] T003 Benchmark candidate local ASR, embedding, VLM, and LLM models on a representative Windows CPU/GPU machine; record accuracy, latency, memory, and model size. `qwen3-vl:4b` passed a three-run smoke benchmark on the corrected synthetic motion fixture: all runs identified a red square moving right; wall times were 4.52 s, 3.77 s, and 3.77 s (about 105 output tokens/s on warm runs). See [environment.md](environment.md). The 20-clip benchmark, peak memory, and representative Windows hardware measurements remain pending.
- [ ] T004 Choose model weights and packaging method from T003; document license and minimum hardware.

## Phase 2: Shared foundation

- [ ] T005 Implement native picker, drag and drop, FFprobe validation, source fingerprint, and project persistence.
- [ ] T006 Implement typed worker jobs with progress, cancellation, structured errors, and recovery.
- [ ] T007 Implement source player, timecode timeline, and source/result state labels.
- [ ] T008 Implement interval algebra and revision history with unit tests for keep, remove, overlap, empty result, undo, and redo.

## Phase 3: US1 — index video

- [ ] T009 Extract analysis audio and create timestamped speech evidence locally.
- [ ] T010 Detect scenes, sample frames, and build a visual embedding index.
- [ ] T011 Verify simple visible actions over short frame sequences using the chosen local VLM.
- [ ] T012 Cache indexes by media fingerprint and model version; demonstrate reopening without reanalysis.

## Phase 4: US2 and US4 — request and refine an edit

- [ ] T013 Parse chat instructions to a validated intent schema; ask for clarification on ambiguous keep/remove intent.
- [ ] T014 Retrieve and rerank speech and visual evidence; create timestamped candidates with reasons and uncertainty.
- [ ] T015 Display candidates on the timeline with evidence, preview, approve/reject, and manual boundary editing.
- [ ] T016 Apply follow-up instructions to the current revision and show an undoable edit history.
- [ ] T017 Run the evaluation set and improve retrieval until SC-001 is met or document the gap and narrow the supported claim.

## Phase 5: US3 — export and inspect

- [ ] T018 Build the FFmpeg export graph from approved intervals; preserve audio/video sync and aspect ratio.
- [ ] T019 Stream export progress, support cancellation, and finalize output only after successful validation.
- [ ] T020 Show final video playback and open-folder action; test MP4, MOV, MKV, silent video, variable frame rate, and multi-segment cuts.

## Phase 6: Release quality

- [ ] T021 Verify offline operation, selected-path confinement, unchanged source hash, and no outbound media traffic.
- [ ] T022 Test clean install, model acquisition, low disk space, missing source, damaged media, and model failure recovery.
- [ ] T023 Package and sign a Windows installer; provide a short first-run guide and publish measured hardware requirements.
