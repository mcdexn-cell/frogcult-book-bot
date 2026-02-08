"""
Provide handlers for main.
"""

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.markup.menu import get_menu_markup
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
async def menu(message: types.Message):
    """
    Show the menu.
    """

    await message.answer(
        'Ви можете підписатися на нові книги за наступними категоріями:',
        reply_markup=get_menu_markup(),
    )


@router.callback_query(F.data == "menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    """
    Show the menu.
    """
    await state.clear()
    await callback.message.edit_text('Ви можете підписатися на нові книги за наступними категоріями:')
    await callback.message.edit_reply_markup(reply_markup=get_menu_markup())
    await callback.answer()


@router.callback_query(F.data == "menu_exit")
async def exit_menu(callback: types.CallbackQuery):
    """
    Exit the menu.
    """
    await callback.message.delete()
