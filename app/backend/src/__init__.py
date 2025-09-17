"""Crypto Tracker Backend Package.

This package contains the FastAPI backend for the Crypto Tracker application.
It provides RESTful API endpoints for cryptocurrency data from CoinMarketCap.
"""

__version__ = "1.0.0"
__author__ = "Crypto Tracker Team"

# Import main components for easier access
from .config import settings
from .http_client import CMCHTTPClient, HTTPClientError
from .models import Cryptocurrency, CryptocurrencyQuote, ErrorResponse

__all__ = [
    "settings",
    "CMCHTTPClient", 
    "HTTPClientError",
    "Cryptocurrency",
    "CryptocurrencyQuote", 
    "ErrorResponse",
]
