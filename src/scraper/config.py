"""
Provide scraping config.
"""

from dataclasses import dataclass
from dataclasses_json import dataclass_json

from src.enums.scraper import ParseMode
from src.structures.scraper import ParserFieldConfig


@dataclass_json
@dataclass
class PublisherConfig:
    name: str
    config: dict[str, ParserFieldConfig]
    book_page_config: dict[str, ParserFieldConfig]
    new_books_url: str | None = None
    preorder_books_url: str | None = None
    coming_soon_books_url: str | None = None
    new_books_config: dict[str, ParserFieldConfig] | None = None
    preorder_books_config: dict[str, ParserFieldConfig] | None = None
    coming_soon_books_config: dict[str, ParserFieldConfig] | None = None


BOOK_CONFIG = {
    'КСД': {
        'title': ParserFieldConfig(selector='.MuiStack-root h1.MuiTypography-root'),
        'author': ParserFieldConfig(selector='.MuiStack-root p:has-text(\'Автор\')  >> xpath=following-sibling::*[1]'),
        'publisher': ParserFieldConfig(selector='.MuiStack-root p:has-text(\'Видавництво\')  >> xpath=following-sibling::*[1]'),
        'isbn': ParserFieldConfig(selector='.MuiStack-root p:has-text(\'ISBN\')  >> xpath=following-sibling::*[1]'),
        'genres': ParserFieldConfig(selector='.MuiStack-root p:has-text(\'Розділ\')  >> xpath=following-sibling::*[1]'),
    },
    'BookChef': {
        'title': ParserFieldConfig(selector='.body_text h1'),
        'author': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Автор\') .val'),
        'publisher': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Видавництво\') .val'),
        'isbn': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'ISBN\') .val'),
        'genres': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Жанр\') .val'),
    }
}


PUBLISHERS_CONFIG = [
    # PublisherConfig(
    #     name='КСД',
    #     config={
    #         'book_urls': ParserFieldConfig(selector='.ui-catalog-card--variant-default', attribute='href', mode=ParseMode.ALL)
    #     },
    #     book_page_config={
    #         'title': ParserFieldConfig(selector='.MuiStack-root h1.MuiTypography-root'),
    #         'author': ParserFieldConfig(selector='[class*="-full-specifications"] p:has-text(\'Автор\')  >> xpath=following-sibling::*[1]'),
    #         'publisher': ParserFieldConfig(selector='[class*="-full-specifications"] p:has-text(\'Видавництво\')  >> xpath=following-sibling::*[1]'),
    #         'isbn': ParserFieldConfig(selector='[class*="-full-specifications"] p:has-text(\'ISBN\')  >> xpath=following-sibling::*[1]'),
    #         'genres': ParserFieldConfig(selector='[class*="-full-specifications"] p:has-text(\'Розділ\')  >> xpath=following-sibling::*[1]'),
    #     },
    #     coming_soon_books_url='https://ksd.ua/books/special/anonsy/page-${page_number}'
    # ),
    PublisherConfig(
        name='BookChef',
        config={
            'book_urls': ParserFieldConfig(selector='.catalog-item-info a.item-title', attribute='href', mode=ParseMode.ALL)
        },
        book_page_config={
            'title': ParserFieldConfig(selector='.body_text h1'),
            'author': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Автор\') .val'),
            'publisher': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Видавництво\') .val'),
            'isbn': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'ISBN\') .val'),
            'genres': ParserFieldConfig(selector='.catalog-detail-property:has-text(\'Жанр\') .val'),
        },
        new_books_url='https://bookchef.ua/catalog/newproduct/?PAGEN_1=${page_number}',
        preorder_books_url='https://bookchef.ua/catalog/preorder/?PAGEN_1=${page_number}'
    )
]
