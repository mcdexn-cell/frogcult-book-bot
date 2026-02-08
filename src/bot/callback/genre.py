"""
Provide genre callback.
"""

from aiogram.filters.callback_data import CallbackData


class GenreCategoryCallback(CallbackData, prefix='genre_category'):
    """
    Genre category callback.
    """
    name: str


class ToggleGenreSubscriptionCallback(CallbackData, prefix='genre'):
    """
    Toggle genre subscription callback.
    """
    id: int
    is_subscribed: bool
