import asyncio
import logging
from typing import Optional
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession, ClientError, ClientResponseError, ClientTimeout
from config import config

logger = logging.getLogger(__name__)
router = Router()


class APIClient:
    """HTTP client for backend API communication."""
    
    @staticmethod
    async def make_request(endpoint: str, timeout: int = None) -> Optional[dict]:
        """Make HTTP request to backend API with error handling."""
        timeout_val = timeout or config.REQUEST_TIMEOUT
        url = f"{config.BACKEND_URL}{endpoint}"
        
        for attempt in range(config.MAX_RETRIES):
            try:
                timeout_obj = ClientTimeout(total=timeout_val)
                async with ClientSession(timeout=timeout_obj) as session:
                    logger.debug(f"Making request to: {url} (attempt {attempt + 1})")
                    async with session.get(url) as response:
                        if response.status == 200:
                            data = await response.json()
                            logger.debug(f"Successful response from {endpoint}")
                            return data
                        elif response.status == 404:
                            logger.warning(f"Resource not found: {endpoint}")
                            return None
                        else:
                            logger.error(f"HTTP {response.status} from {endpoint}")
                            return None
            except ClientResponseError as e:
                logger.error(f"Response error (attempt {attempt + 1}): {e}")
            except ClientError as e:
                logger.error(f"Client error (attempt {attempt + 1}): {e}")
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}): {e}")
            
            if attempt < config.MAX_RETRIES - 1:
                await asyncio.sleep(1)  # Wait before retry
        
        return None


def format_crypto_data(data: dict, detailed: bool = False) -> str:
    """Format cryptocurrency data for display."""
    if not data:
        return "❌ No data available"
    
    name = data.get('name', 'Unknown')
    symbol = data.get('symbol', '')
    
    # Get USD quote data
    usd_quote = data.get('quote', {}).get('USD', {})
    
    if not detailed:
        price = usd_quote.get('price', 0)
        percent_change_24h = usd_quote.get('percent_change_24h', 0)
        
        price_str = f"${price:,.2f}" if price else "N/A"
        change_str = f"{percent_change_24h:+.2f}%" if percent_change_24h is not None else "N/A"
        change_emoji = "📈" if percent_change_24h and percent_change_24h > 0 else "📉" if percent_change_24h and percent_change_24h < 0 else "➡️"
        
        return f"🪙 **{name} ({symbol})**\n💰 Price: {price_str}\n{change_emoji} 24h: {change_str}"
    
    # Detailed format
    price = usd_quote.get('price', 0)
    volume_24h = usd_quote.get('volume_24h', 0)
    market_cap = usd_quote.get('market_cap', 0)
    percent_change_1h = usd_quote.get('percent_change_1h', 0)
    percent_change_24h = usd_quote.get('percent_change_24h', 0)
    percent_change_7d = usd_quote.get('percent_change_7d', 0)
    
    rank = data.get('cmc_rank', 'N/A')
    
    result = f"🪙 **{name} ({symbol})**\n"
    result += f"🏆 Rank: #{rank}\n"
    result += f"💰 Price: ${price:,.2f}" if price else "💰 Price: N/A\n"
    result += f"\n📊 Market Cap: ${market_cap:,.0f}" if market_cap else "\n📊 Market Cap: N/A"
    result += f"\n📈 Volume (24h): ${volume_24h:,.0f}" if volume_24h else "\n📈 Volume (24h): N/A"
    
    if percent_change_1h is not None:
        emoji_1h = "📈" if percent_change_1h > 0 else "📉" if percent_change_1h < 0 else "➡️"
        result += f"\n{emoji_1h} 1h: {percent_change_1h:+.2f}%"
    
    if percent_change_24h is not None:
        emoji_24h = "📈" if percent_change_24h > 0 else "📉" if percent_change_24h < 0 else "➡️"
        result += f"\n{emoji_24h} 24h: {percent_change_24h:+.2f}%"
    
    if percent_change_7d is not None:
        emoji_7d = "📈" if percent_change_7d > 0 else "📉" if percent_change_7d < 0 else "➡️"
        result += f"\n{emoji_7d} 7d: {percent_change_7d:+.2f}%"
    
    return result


@router.message(Command('start'))
async def start_command(message: Message):
    """Handle /start command."""
    welcome_text = (
        "🚀 **Welcome to Crypto Tracker Bot!**\n\n"
        "I can help you track cryptocurrency prices and market data.\n\n"
        "📋 **Available commands:**\n"
        "• /help - Show this help message\n"
        "• /top - Get top 10 cryptocurrencies\n"
        "• /crypto <id> - Get specific crypto by ID\n"
        "• /search <name> - Search for crypto by name\n"
        "• /trending - Get trending cryptocurrencies\n\n"
        "💡 **Examples:**\n"
        "• /crypto 1 - Get Bitcoin data\n"
        "• /crypto 1027 - Get Ethereum data\n"
        "• /top - Get top 10 cryptos\n\n"
        "Happy trading! 📈"
    )
    
    await message.answer(welcome_text, parse_mode="Markdown")


@router.message(Command('help'))
async def help_command(message: Message):
    """Handle /help command."""
    help_text = (
        "📋 **Crypto Tracker Bot Commands:**\n\n"
        "🔝 **/top [limit]** - Get top cryptocurrencies (default: 10, max: 100)\n"
        "🪙 **/crypto <id>** - Get detailed crypto data by CoinMarketCap ID\n"
        "🔍 **/search <name>** - Search cryptocurrencies by name\n"
        "🔥 **/trending** - Get trending cryptocurrencies\n"
        "ℹ️ **/help** - Show this help message\n\n"
        "💡 **Usage Examples:**\n"
        "• `/top` - Top 10 cryptocurrencies\n"
        "• `/top 5` - Top 5 cryptocurrencies\n"
        "• `/crypto 1` - Bitcoin details\n"
        "• `/crypto 1027` - Ethereum details\n\n"
        "📊 **Popular Crypto IDs:**\n"
        "• Bitcoin (BTC): 1\n"
        "• Ethereum (ETH): 1027\n"
        "• Tether (USDT): 825\n"
        "• BNB: 1839\n"
        "• Solana (SOL): 5426\n"
        "• XRP: 52\n"
        "• Dogecoin (DOGE): 74\n"
        "• Cardano (ADA): 2010\n"
    )
    
    await message.answer(help_text, parse_mode="Markdown")


@router.message(Command('top'))
async def top_command(message: Message):
    """Handle /top command to get top cryptocurrencies."""
    try:
        # Parse limit from command
        parts = message.text.split()
        limit = 10  # default
        if len(parts) > 1 and parts[1].isdigit():
            limit = min(max(int(parts[1]), 1), 100)  # Clamp between 1-100
        
        await message.answer("🔄 Fetching top cryptocurrencies...")
        
        data = await APIClient.make_request(f"/cryptocurrency/?limit={limit}")
        
        if not data or 'data' not in data or not data['data']:
            await message.answer("❌ Sorry, I couldn't fetch cryptocurrency data right now. Please try again later.")
            return
        
        cryptos = data['data'][:limit]  # Ensure we don't exceed limit
        
        response = f"🏆 **Top {len(cryptos)} Cryptocurrencies:**\n\n"
        
        for i, crypto in enumerate(cryptos, 1):
            name = crypto.get('name', 'Unknown')
            symbol = crypto.get('symbol', '')
            price = crypto.get('quote', {}).get('USD', {}).get('price', 0)
            change_24h = crypto.get('quote', {}).get('USD', {}).get('percent_change_24h', 0)
            
            price_str = f"${price:,.2f}" if price else "N/A"
            change_emoji = "📈" if change_24h and change_24h > 0 else "📉" if change_24h and change_24h < 0 else "➡️"
            change_str = f"{change_24h:+.2f}%" if change_24h is not None else "N/A"
            
            response += f"{i}. **{name} ({symbol})**\n"
            response += f"   💰 {price_str} {change_emoji} {change_str}\n\n"
        
        if len(response) > 4000:  # Telegram message limit
            response = response[:3900] + "\n\n... (truncated)"
        
        await message.answer(response, parse_mode="Markdown")
    
    except Exception as e:
        logger.error(f"Error in top_command: {e}")
        await message.answer("❌ An error occurred while fetching data. Please try again later.")


@router.message(Command('crypto'))
async def crypto_command(message: Message):
    """Handle /crypto command to get specific cryptocurrency by ID."""
    try:
        parts = message.text.split()
        if len(parts) < 2 or not parts[1].isdigit():
            await message.answer(
                "❌ **Usage:** `/crypto <id>`\n\n"
                "**Examples:**\n"
                "• `/crypto 1` - Bitcoin\n"
                "• `/crypto 1027` - Ethereum\n\n"
                "💡 Use /help to see popular crypto IDs",
                parse_mode="Markdown"
            )
            return
        
        currency_id = int(parts[1])
        
        await message.answer(f"🔄 Fetching data for cryptocurrency #{currency_id}...")
        
        data = await APIClient.make_request(f"/cryptocurrency/{currency_id}")
        
        if not data or 'data' not in data:
            await message.answer(f"❌ Cryptocurrency with ID {currency_id} not found. Please check the ID and try again.")
            return
        
        crypto_data = data['data']
        formatted_data = format_crypto_data(crypto_data, detailed=True)
        
        await message.answer(formatted_data, parse_mode="Markdown")
    
    except ValueError:
        await message.answer("❌ Please provide a valid cryptocurrency ID (number).")
    except Exception as e:
        logger.error(f"Error in crypto_command: {e}")
        await message.answer("❌ An error occurred while fetching data. Please try again later.")


@router.message(Command('trending'))
async def trending_command(message: Message):
    """Handle /trending command - show top 5 with highest 24h change."""
    try:
        await message.answer("🔥 Fetching trending cryptocurrencies...")
        
        data = await APIClient.make_request("/cryptocurrency/?limit=50")
        
        if not data or 'data' not in data or not data['data']:
            await message.answer("❌ Sorry, I couldn't fetch trending data right now. Please try again later.")
            return
        
        # Sort by 24h percent change (highest first)
        cryptos = data['data']
        trending = sorted(
            [c for c in cryptos if c.get('quote', {}).get('USD', {}).get('percent_change_24h') is not None],
            key=lambda x: x.get('quote', {}).get('USD', {}).get('percent_change_24h', 0),
            reverse=True
        )[:5]
        
        if not trending:
            await message.answer("❌ No trending data available right now.")
            return
        
        response = "🔥 **Top 5 Trending (24h gainers):**\n\n"
        
        for i, crypto in enumerate(trending, 1):
            formatted = format_crypto_data(crypto, detailed=False)
            response += f"{i}. {formatted}\n\n"
        
        await message.answer(response, parse_mode="Markdown")
    
    except Exception as e:
        logger.error(f"Error in trending_command: {e}")
        await message.answer("❌ An error occurred while fetching trending data. Please try again later.")


# Legacy command for backward compatibility
@router.message(Command('crypto_id'))
async def crypto_id_command(message: Message):
    """Handle legacy /crypto_id command."""
    # Forward to the new crypto command
    await message.answer("💡 **Note:** `/crypto_id` is deprecated. Please use `/crypto <id>` instead.\n")
    await crypto_command(message)
    