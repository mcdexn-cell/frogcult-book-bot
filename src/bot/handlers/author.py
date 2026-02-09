"""
Provide handlers for author.
"""

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.bot.callback.author import (
    GetAuthorCallbackData,
    ToggleAuthorSubscriptionCallbackData,
)
from src.bot.fsm.author import SearchAuthorForm
from src.bot.markup.authors import (
    get_author_page_markup,
    get_subscribe_authors_markup,
)
from src.bot.markup.menu import get_back_to_menu_markup
from src.bot.service import BookBotService
from src.exceptions.users import AuthorSubscriptionLimitReachedError


router = Router()


@router.callback_query(F.data == 'authors_subscribe')
async def authors_subscribe(callback: types.CallbackQuery):
    """
    Authors subscribe main page.
    """
    await callback.message.edit_text(text='Автори:')
    await callback.message.edit_reply_markup(reply_markup=get_subscribe_authors_markup())
    await callback.answer()


@router.callback_query(F.data == 'list_authors_subscriptions')
async def list_authors_subscriptions(callback: types.CallbackQuery, service: BookBotService):
    """
    List authors subscriptions for user.
    """
    builder = InlineKeyboardBuilder()
    subscribed_authors = await service.list_user_subscribed_authors(user_id=callback.from_user.id)

    if not subscribed_authors:
        await callback.message.edit_text(text='Не знайдено підписок на авторів.')

    else:
        for author in subscribed_authors:
            await callback.message.edit_text(text='Ваші підписки на авторів:')
            builder.button(text=author, callback_data=GetAuthorCallbackData(name=author))

    builder.button(text='⚙ Назад', callback_data='authors_subscribe')

    await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    await callback.answer()


@router.callback_query(GetAuthorCallbackData.filter())
async def get_author_callback_data(
        callback: types.CallbackQuery,
        callback_data: GetAuthorCallbackData,
):
    """
    Get author callback data.
    """
    await callback.message.edit_text(text=f'Сторінка автора: {callback_data.name}')
    await callback.message.edit_reply_markup(reply_markup=get_author_page_markup(name=callback_data.name))
    await callback.answer()


@router.callback_query(ToggleAuthorSubscriptionCallbackData.filter())
async def toggle_author_subscription_callback_data(
        callback: types.CallbackQuery,
        callback_data: ToggleAuthorSubscriptionCallbackData,
        service: BookBotService,
):
    """
    Toggle author subscription callback data.
    """
    try:
        await service.toggle_author_subscription(
            user_id=callback.from_user.id,
            author=callback_data.name,
            is_subscribed=callback_data.is_subscribed,
        )
        await callback.message.edit_text('Статус підписки оновлено успішно.')

    except AuthorSubscriptionLimitReachedError:
        await callback.message.edit_text('Досягнуто ліміту підписок на авторів.')

    await callback.message.edit_reply_markup(reply_markup=get_back_to_menu_markup())
    await callback.answer()


@router.callback_query(F.data == "subscribe_on_author")
async def author_subscribe(callback: types.CallbackQuery, state: FSMContext):
    """
    Find the author to subscribe.
    """
    await callback.message.answer('Введіть ім`я автора:')
    await state.set_state(SearchAuthorForm.waiting_for_input)
    await callback.answer()


@router.message(SearchAuthorForm.waiting_for_input)
async def process_user_author(message: types.Message, state: FSMContext, service: BookBotService):
    """
    Process author message from user.
    """
    author = message.text.title()
    user_authors = await service.list_user_subscribed_authors(user_id=message.from_user.id)
    author_books_count = await service.get_author_books_count(author=author)

    builder = InlineKeyboardBuilder()

    if author in user_authors:
        answer_text = 'Ви вже підписані на цього автора.'

    else:
        if author_books_count > 0:
            answer_text = f'В нашій базі знайдено книг цього автора: {author_books_count}.'

        else:
            answer_text = 'На жаль, в нашій базі ще немає книг цього автора.'

        builder.button(
            text='Підписатися',
            callback_data=ToggleAuthorSubscriptionCallbackData(name=author, is_subscribed=False)
        )

    builder.button(text='⚙ Назад до меню', callback_data='menu')

    await message.answer(answer_text, reply_markup=builder.as_markup())
    await state.clear()
