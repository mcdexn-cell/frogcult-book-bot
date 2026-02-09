"""
Provide markup for genres.
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.callback.genre import (
    GenreCategoryCallback,
    ToggleGenreSubscriptionCallback,
)
from src.bot.constants import IS_SUBSCRIBED_EMOJI_MAP
from src.enums.book import BookGenreCategory
from src.structures.genre import GenreUserContext


def get_genre_categories_keyboard_markup(
        genres_by_category: dict[BookGenreCategory, list[GenreUserContext]]
) -> InlineKeyboardMarkup:
    """
    Get genre categories keyboard markup.

    Args:
        genres_by_category: dict of genres grouped by category.

    Returns:
        genre categories markup.
    """
    builder = InlineKeyboardBuilder()
    for category, genres in genres_by_category.items():
        builder.button(text=category, callback_data=GenreCategoryCallback(name=category).pack())

    builder.button(text='⚙ Назад до меню', callback_data='menu')
    builder.adjust(2)

    return builder.as_markup()


def get_genres_keyboard_markup(genres: list[GenreUserContext]) -> InlineKeyboardMarkup:
    """
    Get genres keyboard markup.

    Args:
        genres: list of genres user context.

    Returns:
        genres markup.
    """
    builder = InlineKeyboardBuilder()

    for genre in genres:
        builder.button(
            text=f'{IS_SUBSCRIBED_EMOJI_MAP[genre.is_subscribed]} {genre.name.value}',
            callback_data=ToggleGenreSubscriptionCallback(id=genre.id, is_subscribed=genre.is_subscribed).pack(),
        )

    builder.button(text='⚙ Назад до категорій', callback_data='genres_subscribe')
    builder.adjust(2)

    return builder.as_markup()
