# Worker API Contract

The browser UI and Python worker share a same-origin HTTP/JSON API. The development server binds to `127.0.0.1` only. API paths include an explicit protocol version; incompatible message changes require a new path such as `/api/v2/`.

## Version 1

`GET /api/v1/health` returns the response described by [worker-v1.schema.json](worker-v1.schema.json):

```json
{
  "protocol_version": 1,
  "status": "ready",
  "worker_version": "0.1.0",
  "capabilities": ["health", "browser_ui"]
}
```

Unknown API paths return a JSON error envelope containing `protocol_version` and an `error` with `code` and `message`. `POST` requests currently return `not_implemented`; job, progress, and cancellation messages will be added with their implementation tasks. Do not send media or prompts to any remote service.
