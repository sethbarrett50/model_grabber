"""Application entrypoint."""

from __future__ import annotations

from model_grabber.cli import run


def main() -> int:
    """Entrypoint used by the console script."""
    return run()


if __name__ == '__main__':
    raise SystemExit(main())
