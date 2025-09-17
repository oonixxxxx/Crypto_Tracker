import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from router import router

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create bot and dispatcher
bot = Bot(
    token=config.TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

# Include router
dp.include_router(router)


async def on_startup():
    """Actions to perform on bot startup."""
    logger.info("🚀 Crypto Tracker Bot is starting up...")
    logger.info(f"Backend URL: {config.BACKEND_URL}")
    logger.info(f"Request timeout: {config.REQUEST_TIMEOUT}s")
    logger.info(f"Max retries: {config.MAX_RETRIES}")


async def on_shutdown():
    """Actions to perform on bot shutdown."""
    logger.info("🛑 Crypto Tracker Bot is shutting down...")
    await bot.session.close()


async def main():
    """Main bot function."""
    try:
        await on_startup()
        logger.info("✅ Bot started successfully! Listening for messages...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Error starting bot: {e}")
        sys.exit(1)
    finally:
        await on_shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)
