"""
Provide dependencies for bot.
"""

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram_broadcaster import Broadcaster

from src.bot.handlers.author import router as author_router
from src.bot.handlers.genre import router as genre_router
from src.bot.handlers.main import router as main_router
from src.bot.handlers.publisher import router as publisher_router
from src.bot.notifier import BookBotNotifierService
from src.dependencies.repositories import get_users_repository
from src.settings import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()

dp.include_routers(
    author_router,
    genre_router,
    main_router,
    publisher_router,
)


def get_bot() -> Bot:
    return bot


def get_dispatcher() -> Dispatcher:
    return dp


def get_broadcaster() -> Broadcaster:
    return Broadcaster(get_bot())


def get_book_bot_notifier() -> BookBotNotifierService:
    return BookBotNotifierService(
        broadcaster=get_broadcaster(),
        users_repository=get_users_repository(),
    )
