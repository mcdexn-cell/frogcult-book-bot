"""
Provide FSM for publishers.
"""

from aiogram.fsm.state import StatesGroup, State


class SearchPublisherForm(StatesGroup):
    """
    Search publisher FSM form.
    """
    waiting_for_input = State()
