"""
Provide callbacks for publishers.
"""

from aiogram.filters.callback_data import CallbackData


class TogglePublisherSubscriptionCallback(CallbackData, prefix='publisher'):
    """
    Toggle publisher subscription callback.
    """
    id: int
    is_subscribed: bool
