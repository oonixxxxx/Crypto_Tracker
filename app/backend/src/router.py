import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import JSONResponse

from . import cmc_client
from .models import ErrorResponse
from .http_client import HTTPClientError

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/cryptocurrency',
    tags=["Cryptocurrency"]
)


@router.get(
    "/",
    summary="Get Cryptocurrency Listings",
    description="Retrieve the latest cryptocurrency market data including prices, market cap, and other metrics.",
    responses={
        200: {"description": "Successful response with cryptocurrency data"},
        503: {"model": ErrorResponse, "description": "Service unavailable - API error"}
    }
)
async def get_cryptocurrency_listings(
    limit: int = Query(
        default=100,
        ge=1,
        le=5000,
        description="Number of results to return (1-5000)"
    ),
    convert: str = Query(
        default="USD",
        description="Currency to convert prices to (e.g., USD, EUR, BTC)"
    )
):
    """Get cryptocurrency listings with optional parameters."""
    try:
        logger.info(f"Fetching cryptocurrency listings: limit={limit}, convert={convert}")
        data = await cmc_client.get_listings(limit=limit, convert=convert)
        return {
            "data": data,
            "count": len(data),
            "limit": limit,
            "convert": convert
        }
    except HTTPClientError as e:
        logger.error(f"Error fetching cryptocurrency listings: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Unable to fetch cryptocurrency data: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in get_cryptocurrency_listings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get(
    "/{currency_id}",
    summary="Get Cryptocurrency by ID",
    description="Retrieve detailed information about a specific cryptocurrency by its CoinMarketCap ID.",
    responses={
        200: {"description": "Successful response with cryptocurrency data"},
        404: {"model": ErrorResponse, "description": "Cryptocurrency not found"},
        503: {"model": ErrorResponse, "description": "Service unavailable - API error"}
    }
)
async def get_cryptocurrency_by_id(
    currency_id: int = Path(
        ...,
        ge=1,
        description="The CoinMarketCap cryptocurrency ID"
    ),
    convert: str = Query(
        default="USD",
        description="Currency to convert prices to (e.g., USD, EUR, BTC)"
    )
):
    """Get specific cryptocurrency by ID."""
    try:
        logger.info(f"Fetching cryptocurrency data for ID: {currency_id}, convert={convert}")
        data = await cmc_client.get_currency(currency_id=currency_id, convert=convert)
        return {
            "data": data,
            "currency_id": currency_id,
            "convert": convert
        }
    except HTTPClientError as e:
        error_msg = str(e)
        if "not found" in error_msg.lower():
            logger.warning(f"Cryptocurrency with ID {currency_id} not found")
            raise HTTPException(
                status_code=404,
                detail=f"Cryptocurrency with ID {currency_id} not found"
            )
        else:
            logger.error(f"Error fetching cryptocurrency {currency_id}: {error_msg}")
            raise HTTPException(
                status_code=503,
                detail=f"Unable to fetch cryptocurrency data: {error_msg}"
            )
    except Exception as e:
        logger.error(f"Unexpected error in get_cryptocurrency_by_id: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
