"""
Provide markup for authors.
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.callback.author import (
    GetAuthorBooksCallbackData,
    ToggleAuthorSubscriptionCallbackData
)


def get_subscribe_authors_markup() -> InlineKeyboardMarkup:
    """
    Get markup for authors subscribe.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text='Переглянути підписки', callback_data='list_authors_subscriptions')
    builder.button(text='Підписатися на автора', callback_data='subscribe_on_author')

    builder.button(text='⚙ Назад до меню', callback_data='menu')

    return builder.as_markup()


def get_author_page_markup(name: str) -> InlineKeyboardMarkup:
    """
    Get markup for author page.
    """
    builder = InlineKeyboardBuilder()

    builder.button(text='Переглянути книги', callback_data=GetAuthorBooksCallbackData(name=name))
    builder.button(
        text='Відписатися',
        callback_data=ToggleAuthorSubscriptionCallbackData(name=name, is_subscribed=True)
    )

    builder.button(text='⚙ Назад', callback_data='list_authors_subscriptions')
    builder.adjust(1)

    return builder.as_markup()
