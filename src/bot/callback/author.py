"""
Provide author callback.
"""

from aiogram.filters.callback_data import CallbackData


class GetAuthorCallbackData(CallbackData, prefix='author'):
    """
    Get author callback data.
    """
    name: str


class GetAuthorBooksCallbackData(CallbackData, prefix='author'):
    """
    Get author books callback data.
    """
    name: str


class ToggleAuthorSubscriptionCallbackData(CallbackData, prefix='author'):
    """
    Toggle author subscription callback data.
    """
    name: str
    is_subscribed: bool
