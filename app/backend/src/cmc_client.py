"""CoinMarketCap API client module."""
import logging
from .http_client import CMCHTTPClient
from .config import settings

logger = logging.getLogger(__name__)

# Initialize the CMC client with settings
cmc_client = CMCHTTPClient(
    base_url=settings.CMC_BASE_URL,
    api_key=settings.CMC_API_KEY
)

logger.info(f"Initialized CMC client with base URL: {settings.CMC_BASE_URL}")


async def get_listings(limit: int = 100, convert: str = 'USD'):
    """Get cryptocurrency listings.
    
    Args:
        limit: Number of results to return (1-5000)
        convert: Currency to convert prices to
        
    Returns:
        List of cryptocurrency data
    """
    return await cmc_client.get_listings(limit=limit, convert=convert)


async def get_currency(currency_id: int, convert: str = 'USD'):
    """Get specific currency by ID.
    
    Args:
        currency_id: The cryptocurrency ID
        convert: Currency to convert prices to
        
    Returns:
        Cryptocurrency data
    """
    return await cmc_client.get_currency(currency_id=currency_id, convert=convert)
