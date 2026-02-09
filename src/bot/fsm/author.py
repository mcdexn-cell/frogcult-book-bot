"""
Provide FSM for authors.
"""

from aiogram.fsm.state import StatesGroup, State


class SearchAuthorForm(StatesGroup):
    """
    Search author FSM form.
    """
    waiting_for_input = State()
