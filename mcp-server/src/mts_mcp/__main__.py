from __future__ import annotations

import asyncio
import sys

from mts_mcp.config import settings
from mts_mcp.server import run


def main() -> None:
    cfg = settings()
    if not cfg.project_root.exists():
        print(f"Projektroot existiert nicht: {cfg.project_root}", file=sys.stderr)
        sys.exit(1)
    asyncio.run(run(cfg))


if __name__ == "__main__":
    main()
