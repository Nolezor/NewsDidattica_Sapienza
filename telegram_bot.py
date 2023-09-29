import asyncio
from telegram import Bot

TOKEN = "<TOKEN>"
CHAT_ID = "<CHAT_ID>"


def get_token():
    return TOKEN


async def send_message(message: str):
    async with Bot(TOKEN) as bot:
        status = await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML")
        print(status)


async def main():
    async with Bot(TOKEN) as bot:
        status = await bot.send_message(chat_id=CHAT_ID, text="Test!", parse_mode="HTML")
        print(status)

if __name__ == '__main__':
    asyncio.run(main())
