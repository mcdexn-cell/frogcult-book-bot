"""
Provide markup for books.
"""
from string import Template

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_broadcaster.contents import TextContent

from src.enums.book import BOOK_STATUS_UKRAINIAN_TEXT
from src.structures.book import Book


BOOK_ALERT_TEMPLATE = Template("""
<b>Нова книга за вашими вподобаннями!</b>

<b>${author}</b> - ${title}

Видавництво: ${publisher}
Статус: ${status}
""")


def get_book_url_markup(url: str) -> InlineKeyboardMarkup:
    """
    Get book url markup

    Args:
        url: book URL to create markup.

    Returns:
        InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()

    builder.button(text='Посилання на магазин', url=url)

    return builder.as_markup()


def get_book_notification_message(book: Book) -> TextContent:
    """
    Get book notification message.
    """
    alert_text = BOOK_ALERT_TEMPLATE.substitute(
        author=book.author,
        title=book.title,
        publisher=book.publisher,
        status=BOOK_STATUS_UKRAINIAN_TEXT[book.status],
    )
    alert_markup = get_book_url_markup(url=book.url)

    return TextContent(
        text=alert_text,
        reply_markup=alert_markup,
        parse_mode='HTML',
    )
