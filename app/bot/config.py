import os
from typing import Optional
from pydantic import BaseModel, Field, validator


class BotConfig(BaseModel):
    """Bot configuration with validation."""
    
    TOKEN: str = Field(..., description="Telegram bot token")
    BACKEND_URL: str = Field(
        default="http://localhost:8000",
        description="Backend API URL"
    )
    REQUEST_TIMEOUT: int = Field(
        default=10,
        description="HTTP request timeout in seconds"
    )
    MAX_RETRIES: int = Field(
        default=3,
        description="Maximum number of retry attempts"
    )
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    @validator('TOKEN')
    def validate_token(cls, v):
        """Validate Telegram bot token format."""
        if not v or len(v) < 10 or ':' not in v:
            raise ValueError('TOKEN must be a valid Telegram bot token')
        return v
    
    @validator('BACKEND_URL')
    def validate_backend_url(cls, v):
        """Validate backend URL format."""
        if not v.startswith(('http://', 'https://')):
            raise ValueError('BACKEND_URL must start with http:// or https://')
        return v.rstrip('/')  # Remove trailing slash
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'LOG_LEVEL must be one of: {", ".join(valid_levels)}')
        return v.upper()


# Load configuration
config = BotConfig(
    TOKEN=os.getenv('TELEGRAM_BOT_TOKEN', ''),
    BACKEND_URL=os.getenv('BACKEND_URL', 'http://localhost:8000'),
    REQUEST_TIMEOUT=int(os.getenv('REQUEST_TIMEOUT', '10')),
    MAX_RETRIES=int(os.getenv('MAX_RETRIES', '3')),
    LOG_LEVEL=os.getenv('LOG_LEVEL', 'INFO')
)
