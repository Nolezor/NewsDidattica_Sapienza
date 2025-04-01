import asyncio
import os
import logging
import sys
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError, NetworkError, TimedOut

if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

logger = logging.getLogger('news_didattica_telegram')

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


def get_token():
    """Return the Telegram bot token from environment variables."""
    return TOKEN


async def send_message(message: str):
    """Send a message to the configured Telegram channel.
    
    Args:
        message (str): The message to send in Markdown format
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    if not TOKEN or not CHAT_ID:
        logger.error("BOT_TOKEN or CHAT_ID environment variables are not set.")
        logger.error("Please create a .env file with BOT_TOKEN and CHAT_ID variables.")
        return False
    
    try:
        logger.info("Attempting to send message to Telegram")
        async with Bot(TOKEN) as bot:
            status = await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="MarkdownV2")
            logger.info(f"Message sent successfully: {status.message_id}")
            return True
            
    except TimedOut:
        logger.error("Timeout while connecting to Telegram. The server might be slow or unresponsive.")
    except NetworkError:
        logger.error("Network error while sending message to Telegram. Check your internet connection.")
    except TelegramError as e:
        logger.error(f"Telegram API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error while sending message: {str(e)}")
    
    return False


# Purely for testing purpose
async def main():
    """Test function to verify the Telegram bot connection.
    Sends a test message to the configured channel.
    """
    if not TOKEN or not CHAT_ID:
        logger.error("BOT_TOKEN or CHAT_ID environment variables are not set.")
        logger.error("Please create a .env file with BOT_TOKEN and CHAT_ID variables.")
        return
    
    try:
        logger.info("Testing Telegram bot connection")
        async with Bot(TOKEN) as bot:
            status = await bot.send_message(chat_id=CHAT_ID, text="**Test!**", parse_mode="MarkdownV2")
            logger.info(f"Test message sent successfully: {status.message_id}")
            
    except Exception as e:
        logger.error(f"Error during test: {str(e)}")


if __name__ == '__main__':
    asyncio.run(main())
