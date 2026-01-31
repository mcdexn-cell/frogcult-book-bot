"""
Provide keyboard builders.
"""
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_back_to_menu_markup() -> InlineKeyboardMarkup:
    """
    Get back to menu keyboard markup.
    """

    builder = InlineKeyboardBuilder()
    builder.button(text='⚙ Назад до меню', callback_data='menu')

    return builder.as_markup()


def get_menu_markup() -> InlineKeyboardMarkup:
    """
    Get main menu markup.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text='🏢 Видавництва', callback_data='publishers_subscribe')
    builder.button(text='🎭 Жанри', callback_data='genres_subscribe')
    builder.button(text='👤 Автори', callback_data='authors_subscribe')
    builder.button(text='➜] Вихід', callback_data='menu_exit')
    builder.adjust(2)

    return builder.as_markup()
