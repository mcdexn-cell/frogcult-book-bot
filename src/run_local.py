"""
Run the bot locally.
"""
import asyncio

from src.dependencies.bot import (
    get_bot,
    get_dispatcher,
)
from src.dependencies.services import get_book_bot_service

dp = get_dispatcher()
bot = get_bot()


async def main():
    service = await get_book_bot_service()
    await dp.start_polling(bot, service=service)


if __name__ == "__main__":
    asyncio.run(main())
