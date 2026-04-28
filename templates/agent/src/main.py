"""Entry point — start the API server or CLI."""

from __future__ import annotations

import sys

import uvicorn

from src.config import settings


def main() -> None:
    if "--cli" in sys.argv:
        from src.cli import main as cli_main
        cli_main()
    else:
        uvicorn.run(
            "src.server:app",
            host="0.0.0.0",
            port=settings.port,
            reload=settings.env == "development",
        )


if __name__ == "__main__":
    main()
