import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .router import router as cryptocurrency_router
from .cmc_client import cmc_client
from .http_client import HTTPClientError

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting Crypto Tracker API...")
    yield
    logger.info("Shutting down Crypto Tracker API...")
    # Close HTTP client session
    try:
        await cmc_client.close()
        logger.info("HTTP client session closed")
    except Exception as e:
        logger.error(f"Error closing HTTP client: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for HTTPClientError
@app.exception_handler(HTTPClientError)
async def http_client_exception_handler(request, exc: HTTPClientError):
    """Handle HTTP client errors."""
    logger.error(f"HTTP client error: {str(exc)}")
    return JSONResponse(
        status_code=503,
        content={
            "detail": "Service temporarily unavailable",
            "error": str(exc)
        }
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "service": "crypto-tracker-api"
    }


# Include routers
app.include_router(cryptocurrency_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
