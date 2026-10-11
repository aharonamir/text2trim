"""Text2Trim local worker package."""

__version__ = "0.1.0"


def main() -> None:
    """Start the loopback development UI and worker API."""
    from .server import serve

    serve()
