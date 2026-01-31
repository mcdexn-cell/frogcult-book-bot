"""
Provide dependencies for bot.
"""

from aiogram import (
    Bot,
    Dispatcher,
)
from src.bot.handlers.main import router as main_router
from src.settings import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()

dp.include_routers(
    main_router,
)


def get_bot():
    return bot


def get_dispatcher():
    return dp
