"""
Provide handler for publishers.
"""

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.markup.menu import get_back_to_menu_markup
from src.bot.callback.publisher import TogglePublisherSubscriptionCallback
from src.bot.constants import IS_SUBSCRIBED_EMOJI_MAP
from src.bot.fsm.publisher import SearchPublisherForm
from src.bot.service import BookBotService


router = Router()


@router.callback_query(F.data == "publishers_subscribe")
async def publishers_subscribe(callback: types.CallbackQuery, state: FSMContext):
    """
    Exit the menu.
    """
    await callback.message.answer('Введіть назву видавництва, що вас цікавить:')
    await state.set_state(SearchPublisherForm.waiting_for_input)
    await callback.answer()


@router.message(SearchPublisherForm.waiting_for_input)
async def process_user_publisher(message: types.Message, state: FSMContext, service: BookBotService):
    """
    Process publisher message from user.
    """
    publishers = await service.search_publishers_for_user(input_text=message.text, user_id=message.from_user.id)

    builder = InlineKeyboardBuilder()

    if not publishers:
        answer_text = 'На жаль, не знайдено видавництв за вашим запитом'

    else:
        answer_text = (
            f'За вашим запитом знайдено видавництв: {len(publishers)}\n'
            f'Натисніть на назву щоб змінити статус підписки.'
        )
        for publisher in publishers:
            emoji = IS_SUBSCRIBED_EMOJI_MAP[publisher.is_subscribed]
            builder.button(
                text=f'{emoji} {publisher.name}',
                callback_data=TogglePublisherSubscriptionCallback(
                    id=publisher.id,
                    is_subscribed=publisher.is_subscribed
                )
            )

        if len(publishers) > 1:
            builder.adjust(2)

    builder.button(text='⚙ Назад до меню', callback_data='menu')

    await message.answer(answer_text, reply_markup=builder.as_markup())
    await state.clear()


@router.callback_query(TogglePublisherSubscriptionCallback.filter())
async def toggle_publisher_subscription(
        query: types.CallbackQuery,
        callback_data: TogglePublisherSubscriptionCallback,
        service: BookBotService,
):
    """
    Toggle publisher subscription callback handler.
    """
    await service.toggle_publisher_subscription(
        user_id=query.from_user.id,
        is_subscribed=callback_data.is_subscribed,
        publisher_id=callback_data.id,
    )

    await query.message.edit_text(text='Статус підписки оновлено успішно.')
    await query.message.edit_reply_markup(reply_markup=get_back_to_menu_markup())
