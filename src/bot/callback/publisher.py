"""
Provide callbacks for publishers.
"""

from aiogram.filters.callback_data import CallbackData


class TogglePublisherSubscriptionCallback(CallbackData, prefix='publisher'):
    """
    Toggle publisher subscription callback.
    """
    publisher: str
    is_subscribed: bool
