# Feature Specification: Natural-language video trimming

**Status**: Draft for implementation  
**Created**: 2026-10-10  
**Target**: Windows desktop, single user, local processing

## Problem and outcome

A user has a video and knows what they want to keep or remove, but does not know the exact timecodes. They should be able to choose a local file, describe the desired content in ordinary language, inspect the proposed edit, and export a playable video.

## User scenarios and acceptance testing

### US1 (P1): Import and understand a video

Given a supported local video, when the user selects it with a file picker or drag and drop, then the app shows duration, resolution, a playable source preview, and staged progress for audio and visual indexing. The source file remains intact. An unsupported or unreadable file produces an actionable error.

### US2 (P1): Keep or cut by natural language

Given an indexed video, when the user asks, for example, “Keep the part where she explains the refund” or “Remove the shots of the red car,” then the app returns one or more candidate source-time ranges, a short reason and evidence for each, and a preview of the resulting edit. The user can confirm, reject, or adjust ranges before export.

### US3 (P1): Export and inspect the result

Given a confirmed edit, when the user chooses an output path and starts export, then the app shows stage and percentage where measurable, supports cancellation, and presents a playable result and “open folder” action when complete. An interrupted export does not replace a prior completed output.

### US4 (P2): Refine through chat

Given a proposed or confirmed edit, when the user says “also remove the silent pause” or “keep a little more before that scene,” then the app revises the same project, shows the new keep ranges and undo history, and never silently discards a previous decision.

## Functional requirements

- **FR-001**: Select one local source video through a native picker or drag and drop. “Upload” means selecting a local file; no network transfer is required.
- **FR-002**: Support MP4, MOV, and MKV inputs containing a video stream; detect and report unsupported codecs or damaged files. Handle clips with or without audio.
- **FR-003**: Show source preview, duration, a timeline with source timecodes, and a separate result preview.
- **FR-004**: Build local, timestamped evidence from speech transcription and sampled visual content, including scene boundaries. The visual path must support requests about visible objects and scenes; action requests must be evaluated against temporal evidence, not one still frame alone.
- **FR-005**: Accept free-text “keep,” “remove,” and follow-up instructions. If intent is unclear, ask for clarification instead of guessing.
- **FR-006**: Translate instructions into ordered, non-overlapping source-time ranges. “Keep” selects matching ranges; “remove” subtracts matching ranges from the current edit. Show the interpretation in plain language.
- **FR-007**: Link every suggested range to the transcript snippet or visual evidence and a confidence/uncertainty indicator. Low-confidence or multiple plausible matches require user selection.
- **FR-008**: Allow add, remove, resize, and reorder of proposed ranges; provide undo/redo and a reset to the full source.
- **FR-009**: Render a local MP4 result with synchronized audio and video; preserve source aspect ratio and frame rate when practical. Let the user choose output path and quality preset.
- **FR-010**: Show distinct progress for probing, audio transcription, visual analysis, matching, preview preparation, and export. Allow cancellation and error recovery.
- **FR-011**: Save a lightweight project containing the source path, media fingerprint, indexes, chat history, edit decisions, and export settings. Reopen it without repeating analysis if the source fingerprint matches.
- **FR-012**: Process media and inference locally by default. No video, frames, transcript, or prompt is sent to a remote service. Model acquisition may need a one-time download, with size and source shown before download.
- **FR-013**: Never overwrite the source. Use a temporary output and atomic finalization when export succeeds.

## Key entities

- **Project**: source reference and fingerprint, index status, conversation, edit revisions, export settings.
- **Evidence**: timestamped transcript span, sampled frame/scene description, or temporal action observation, with provenance.
- **Candidate match**: instruction, source-time interval, evidence IDs, confidence, and review state.
- **Edit decision**: ordered keep intervals plus instruction history and manual changes.
- **Job**: stage, progress, logs, cancel state, and recoverable error.

## Edge cases

- A request matches nothing, many places, or contradictory evidence: show candidates or a clarification prompt; do not generate an empty result silently.
- A silent video can still be searched visually. A visually ambiguous request can be anchored by speech, timecode, or manual range selection.
- Multiple audio streams, variable frame rate, rotation metadata, nonzero source timestamps, and cuts near keyframes must not create drift or unexpected extra frames.
- Low disk space, model unavailable, missing source after project reopen, and cancellation leave an understandable state and no corrupt final file.
- Prompt text or transcript content cannot invoke arbitrary shell commands, read other files, or change app settings.

## Non-functional requirements and success criteria

- **SC-001**: On the defined test set of 20 short clips (speech, visible objects/scenes, simple actions, silent footage), at least 18 of 20 requests return the correct event among at most three candidates. Record the dataset and scoring rubric before tuning.
- **SC-002**: For approved boundaries, exported cuts are within 0.25 seconds of the selected timecodes and audio/video sync is within 0.1 seconds on the test set.
- **SC-003**: A user can import, request, review, and start export without using the command line. Every long-running stage reports progress or an indeterminate state within 2 seconds.
- **SC-004**: With models installed, a normal editing session works with network access disabled. Source file hashes before and after are identical.
- **SC-005**: Exported MP4s play in the app and a standard Windows player for every supported test fixture.

## Assumptions and scope

- Windows 10/11 desktop is the first target; one project contains one source video.
- A local model can run on CPU, with acceleration when available. Hardware minimums and timing targets will be set after a benchmark spike.
- The first release supports spoken content, objects, scenes, and simple visible actions. Complex intent such as “all the exciting moments” needs review and may produce multiple candidates.
- No account, cloud sync, collaboration, subtitles, transitions, or social publishing in the first release.

## Open decisions

1. Which languages must speech and chat support at launch?
2. What are the maximum expected video duration/resolution and minimum PC specifications?
3. Must the installer include model weights, or may first-run setup download them?
4. What should happen if a user combines contradictory keep and remove instructions? Proposed rule: latest explicit instruction wins, shown in the edit history.
