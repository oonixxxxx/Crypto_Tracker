import uvicorn

from .config import settings


def main() -> None:
    uvicorn.run(
        "app.backend.src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()


