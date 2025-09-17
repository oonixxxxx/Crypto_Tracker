"""Data models for the Crypto Tracker API."""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class CryptocurrencyQuote(BaseModel):
    """Model for cryptocurrency quote data."""
    price: float = Field(..., description="Current price")
    volume_24h: Optional[float] = Field(None, description="24-hour volume")
    volume_change_24h: Optional[float] = Field(None, description="24-hour volume change")
    percent_change_1h: Optional[float] = Field(None, description="1-hour price change percentage")
    percent_change_24h: Optional[float] = Field(None, description="24-hour price change percentage")
    percent_change_7d: Optional[float] = Field(None, description="7-day price change percentage")
    market_cap: Optional[float] = Field(None, description="Market capitalization")
    market_cap_dominance: Optional[float] = Field(None, description="Market cap dominance")
    fully_diluted_market_cap: Optional[float] = Field(None, description="Fully diluted market cap")
    last_updated: datetime = Field(..., description="Last update timestamp")


class Cryptocurrency(BaseModel):
    """Model for cryptocurrency data."""
    id: int = Field(..., description="Cryptocurrency ID")
    name: str = Field(..., description="Cryptocurrency name")
    symbol: str = Field(..., description="Cryptocurrency symbol")
    slug: str = Field(..., description="Cryptocurrency slug")
    cmc_rank: Optional[int] = Field(None, description="CoinMarketCap rank")
    num_market_pairs: Optional[int] = Field(None, description="Number of market pairs")
    circulating_supply: Optional[float] = Field(None, description="Circulating supply")
    total_supply: Optional[float] = Field(None, description="Total supply")
    max_supply: Optional[float] = Field(None, description="Maximum supply")
    infinite_supply: Optional[bool] = Field(None, description="Whether supply is infinite")
    last_updated: datetime = Field(..., description="Last update timestamp")
    date_added: datetime = Field(..., description="Date added to CoinMarketCap")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags")
    platform: Optional[Dict] = Field(None, description="Platform information")
    self_reported_circulating_supply: Optional[float] = Field(None, description="Self-reported circulating supply")
    self_reported_market_cap: Optional[float] = Field(None, description="Self-reported market cap")
    quote: Dict[str, CryptocurrencyQuote] = Field(..., description="Price quotes in different currencies")


class CryptocurrencyList(BaseModel):
    """Model for cryptocurrency listings response."""
    data: List[Cryptocurrency] = Field(..., description="List of cryptocurrencies")
    status: Dict = Field(..., description="API response status")


class CryptocurrencyDetail(BaseModel):
    """Model for single cryptocurrency detail response."""
    data: Dict[str, Cryptocurrency] = Field(..., description="Cryptocurrency data by ID")
    status: Dict = Field(..., description="API response status")


class ErrorResponse(BaseModel):
    """Model for API error responses."""
    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
