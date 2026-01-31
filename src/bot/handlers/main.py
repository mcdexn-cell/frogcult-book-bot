"""
Provide handlers for main.
"""

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.service import BookBotService


router = Router()


@router.message(Command('start'))
async def start(message: types.Message, service: BookBotService):
    """
    Start the bot.
    """
    reply_message = (
        f'Вітаємо у Frog Cult Book Bot!\n'
        f'Цей бот допоможе вам відстежувати нові книги та передзамовлення за вашими вподобаннями.'
    )
    await service.register(user_id=message.from_user.id)
    await message.answer(reply_message)


@router.message(Command('menu'))
async def menu(message: types.Message, service: BookBotService):
    """
    Show the menu.
    """
    builder = InlineKeyboardBuilder()
    builder.button(text='🏢 Видавництва', callback_data='publishers_callback')
    builder.button(text='🎭 Жанри', callback_data='genres_callback')
    builder.button(text='👤 Автори', callback_data='authors_callback')
    builder.button(text='➜] Вихід', callback_data='menu_exit')
    builder.adjust(2)

    await message.answer(
        'Ви можете підписатися на нові книги за наступними категоріями:',
        reply_markup=builder.as_markup(),
    )


@router.callback_query(F.data == "menu_exit")
async def exit_menu(callback: types.CallbackQuery):
    """
    Exit the menu.
    """
    await callback.message.delete()
