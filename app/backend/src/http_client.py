import logging
from typing import Dict, Any, Optional
from aiohttp import ClientSession, ClientError, ClientResponseError
from .config import settings

logger = logging.getLogger(__name__)


class HTTPClientError(Exception):
    """Custom exception for HTTP client errors."""
    pass


class HTTPClient:
    """Base HTTP client with error handling."""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = ClientSession(
            base_url=self.base_url,
            headers={
                'X-CMC_PRO_API_KEY': api_key,
                'Accept': 'application/json'
            },
            timeout=30
        )
    
    async def close(self):
        """Close the HTTP session."""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class CMCHTTPClient(HTTPClient):
    """CoinMarketCap API HTTP client."""
    
    async def get_listings(self, limit: int = 100, convert: str = 'USD') -> Dict[str, Any]:
        """Get cryptocurrency listings.
        
        Args:
            limit: Number of results to return (1-5000)
            convert: Currency to convert prices to
            
        Returns:
            Dictionary containing cryptocurrency listings
            
        Raises:
            HTTPClientError: If API request fails
        """
        try:
            params = {
                'limit': min(max(limit, 1), 5000),  # Ensure limit is within valid range
                'convert': convert
            }
            
            async with self.session.get(
                url='/v1/cryptocurrency/listings/latest',
                params=params
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                if result.get('status', {}).get('error_code') != 0:
                    error_message = result.get('status', {}).get('error_message', 'Unknown API error')
                    logger.error(f"CMC API error: {error_message}")
                    raise HTTPClientError(f"CMC API error: {error_message}")
                
                logger.info(f"Successfully fetched {len(result.get('data', []))} cryptocurrency listings")
                return result['data']
                
        except ClientResponseError as e:
            logger.error(f"HTTP error getting listings: {e.status} - {e.message}")
            raise HTTPClientError(f"HTTP error: {e.status} - {e.message}")
        except ClientError as e:
            logger.error(f"Client error getting listings: {str(e)}")
            raise HTTPClientError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error getting listings: {str(e)}")
            raise HTTPClientError(f"Unexpected error: {str(e)}")
    
    async def get_currency(self, currency_id: int, convert: str = 'USD') -> Dict[str, Any]:
        """Get specific currency by ID.
        
        Args:
            currency_id: The cryptocurrency ID
            convert: Currency to convert prices to
            
        Returns:
            Dictionary containing cryptocurrency data
            
        Raises:
            HTTPClientError: If API request fails
        """
        try:
            params = {
                'id': currency_id,
                'convert': convert
            }
            
            async with self.session.get(
                url='/v2/cryptocurrency/quotes/latest',
                params=params
            ) as response:
                response.raise_for_status()
                result = await response.json()
                
                if result.get('status', {}).get('error_code') != 0:
                    error_message = result.get('status', {}).get('error_message', 'Unknown API error')
                    logger.error(f"CMC API error for currency {currency_id}: {error_message}")
                    raise HTTPClientError(f"CMC API error: {error_message}")
                
                currency_data = result['data'].get(str(currency_id))
                if not currency_data:
                    logger.error(f"Currency with ID {currency_id} not found")
                    raise HTTPClientError(f"Currency with ID {currency_id} not found")
                
                logger.info(f"Successfully fetched data for currency ID {currency_id}")
                return currency_data
                
        except ClientResponseError as e:
            logger.error(f"HTTP error getting currency {currency_id}: {e.status} - {e.message}")
            raise HTTPClientError(f"HTTP error: {e.status} - {e.message}")
        except ClientError as e:
            logger.error(f"Client error getting currency {currency_id}: {str(e)}")
            raise HTTPClientError(f"Network error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error getting currency {currency_id}: {str(e)}")
            raise HTTPClientError(f"Unexpected error: {str(e)}")
