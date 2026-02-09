"""
Provide handlers for genres.
"""
from collections import defaultdict

from aiogram import (
    F,
    Router,
    types,
)
from aiogram.fsm.context import FSMContext

from src.bot.callback.genre import (
    GenreCategoryCallback,
    ToggleGenreSubscriptionCallback,
)
from src.bot.markup.genres import (
    get_genres_keyboard_markup,
    get_genre_categories_keyboard_markup,
)
from src.bot.markup.menu import get_back_to_menu_markup
from src.bot.service import BookBotService


router = Router()


@router.callback_query(F.data == "genres_subscribe")
async def genres_subscribe(callback: types.CallbackQuery, service: BookBotService, state: FSMContext):
    """
    Open list of genre categories.
    """
    genres = await service.list_genres_for_user(user_id=callback.from_user.id)
    genres_by_category = defaultdict(list)
    for genre in genres:
        genres_by_category[genre.category].append(genre)

    await state.update_data(genres_by_category=genres_by_category)

    await callback.message.edit_text(
        text='Оберіть категорію жанрів:',
        reply_markup=get_genre_categories_keyboard_markup(genres_by_category=genres_by_category),
    )
    await callback.answer()


@router.callback_query(GenreCategoryCallback.filter())
async def genre_category_callback(
        callback: types.CallbackQuery,
        callback_data: GenreCategoryCallback,
        state: FSMContext,
):
    """
    Genre category selected callback: list genres.
    """
    state_data = await state.get_data()
    genres_by_category = state_data['genres_by_category']

    await callback.message.edit_text(
        text=f'Жанри категорії {callback_data.name}:',
        reply_markup=get_genres_keyboard_markup(genres=genres_by_category[callback_data.name]),
    )
    await callback.answer()


@router.callback_query(ToggleGenreSubscriptionCallback.filter())
async def toggle_genre_subscription_callback(
        callback: types.CallbackQuery,
        callback_data: ToggleGenreSubscriptionCallback,
        service: BookBotService,
):
    """
    Genre selected callback: toggle genre subscription.
    """
    await service.toggle_genre_subscription(
        user_id=callback.from_user.id,
        genre_id=callback_data.id,
        is_subscribed=callback_data.is_subscribed,
    )
    await callback.message.edit_text(
        text='Статус підписки оновлено успішно.',
        reply_markup=get_back_to_menu_markup(),
    )
    await callback.answer()
