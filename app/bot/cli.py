import asyncio
import sys

from .bot import main as run_bot


def main() -> None:
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()


