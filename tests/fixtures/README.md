# Fixture and Evaluation Format

Keep evaluation media small and licensed for redistribution. Store each case's metadata in `cases.jsonl`, one UTF-8 JSON object per line. Media paths are relative to this directory; never use external paths or include user media.

Each object uses this shape:

```json
{
  "id": "synthetic-red-motion-001",
  "media": "media/synthetic-red-motion.mp4",
  "sha256": "<64 lowercase hex characters>",
  "license": {"spdx_id": "CC0-1.0", "source": "generated in this repository"},
  "duration_ms": 4000,
  "tags": ["silent", "object", "action"],
  "query": "Keep the part where a red square moves across the frame.",
  "expected": [{"start_ms": 0, "end_ms": 4000, "evidence": "red square moves left to right"}]
}
```

Use SPDX license identifiers and provide a source or attribution for every imported asset. For each case, record the expected source-time interval(s), query, and tags from `speech`, `scene`, `object`, `action`, and `silent`. Add codec, dimensions, and frame rate when relevant to a media edge case. Hash the exact checked-in media with SHA-256. Generated fixtures must include their generation command and parameters in this file or a nearby fixture note. The initial synthetic case is silent and tests only basic visual motion; it does not validate speech understanding or model accuracy.

## Initial synthetic fixture

`media/synthetic-red-motion.mp4` is a 4-second, 320×180, 10 fps H.264 clip generated locally with FFmpeg; a red square moves left-to-right in four timed positions on a gray background. It is original generated material dedicated under CC0-1.0. Recreate it with:

```bash
ffmpeg -hide_banner -loglevel error -y -f lavfi -i 'color=c=gray:s=320x180:r=10:d=4' -vf "drawbox=x=20:y=70:w=30:h=30:color=red:t=fill:enable=lt(t\,1),drawbox=x=90:y=70:w=30:h=30:color=red:t=fill:enable=gte(t\,1)*lt(t\,2),drawbox=x=160:y=70:w=30:h=30:color=red:t=fill:enable=gte(t\,2)*lt(t\,3),drawbox=x=240:y=70:w=30:h=30:color=red:t=fill:enable=gte(t\,3)" -an -c:v libx264 -preset ultrafast -crf 30 -pix_fmt yuv420p -movflags +faststart media/synthetic-red-motion.mp4
```

The corpus target is 20 short clips spanning speech, scenes, visible objects, simple actions, and silent footage. Keep evaluation labels fixed before tuning retrieval, and document the scoring rubric alongside results.
