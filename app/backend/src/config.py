import os
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # CoinMarketCap API configuration
    CMC_API_KEY: str = Field(..., description="CoinMarketCap API key")
    CMC_BASE_URL: str = Field(
        default="https://pro-api.coinmarketcap.com",
        description="CoinMarketCap API base URL"
    )
    
    # Server configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # API configuration
    API_TITLE: str = Field(default="Crypto Tracker API", description="API title")
    API_VERSION: str = Field(default="1.0.0", description="API version")
    API_DESCRIPTION: str = Field(
        default="A FastAPI application for tracking cryptocurrency data",
        description="API description"
    )
    
    # Rate limiting and timeouts
    REQUEST_TIMEOUT: int = Field(default=30, description="HTTP request timeout in seconds")
    CACHE_TTL: int = Field(default=300, description="Cache TTL in seconds")
    
    # Logging configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    @validator('CMC_API_KEY')
    def validate_api_key(cls, v):
        """Validate CMC API key format."""
        if not v or len(v) < 10:
            raise ValueError('CMC_API_KEY must be a valid API key')
        return v
    
    @validator('PORT')
    def validate_port(cls, v):
        """Validate port number."""
        if v < 1 or v > 65535:
            raise ValueError('PORT must be between 1 and 65535')
        return v
    
    @validator('LOG_LEVEL')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'LOG_LEVEL must be one of: {", ".join(valid_levels)}')
        return v.upper()
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )


# Create settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    raise
