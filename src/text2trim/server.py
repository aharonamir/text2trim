"""Loopback-only HTTP server for the browser UI and versioned worker API."""

from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from . import __version__

WEB_ROOT = Path(__file__).resolve().parents[2] / "web"
PROTOCOL_VERSION = 1
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


class Text2TrimHandler(SimpleHTTPRequestHandler):
    """Serve static UI files and the v1 JSON API from one local origin."""

    server_version = "Text2Trim/0.1"

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)  # type: ignore[arg-type]

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/v1/health":
            self._send_json(
                200,
                {
                    "protocol_version": PROTOCOL_VERSION,
                    "status": "ready",
                    "worker_version": __version__,
                    "capabilities": ["health", "browser_ui"],
                },
            )
            return
        if path.startswith("/api/"):
            self._send_error_json(404, "not_found", "Unknown API endpoint.")
            return
        super().do_GET()

    def do_POST(self) -> None:
        self._send_error_json(
            501,
            "not_implemented",
            "Worker job operations are not implemented yet.",
        )

    def end_headers(self) -> None:
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; connect-src 'self'; media-src 'self' blob:; "
            "object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
        )
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, status: int, code: str, message: str) -> None:
        self._send_json(
            status,
            {
                "protocol_version": PROTOCOL_VERSION,
                "error": {"code": code, "message": message},
            },
        )


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Serve the app on loopback without exposing it to the network."""
    if not WEB_ROOT.is_dir():
        raise RuntimeError(f"Web UI directory is missing: {WEB_ROOT}")

    server = ThreadingHTTPServer((host, port), Text2TrimHandler)
    print(
        f"Text2Trim is available at http://{host}:{server.server_port} (Ctrl+C to stop)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Stopping Text2Trim")
    finally:
        server.server_close()
