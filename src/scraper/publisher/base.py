"""
Provide base publisher scraper.
"""
import asyncio
from string import Template
from typing import AsyncIterator
from urllib.parse import urlparse

from src.enums.book import BookStatus
from src.structures.book import Book
from src.scraper.book.base import BaseBookScraper
from src.scraper.config import PublisherConfig
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.utils import parse_config
from src.structures.scraper import ParserFieldConfig


class BasePublisherScraper:
    """
    Base publisher scraper.
    """
    def __init__(
        self,
        scraper_engine: PlaywrightScraperEngine,
        config: PublisherConfig,
        book_scraper: BaseBookScraper,
    ):
        """
        Construct the object.

        Args:
            config: publisher config.
            book_scraper: book scraper.
        """
        self._scraper = scraper_engine
        self._config = config
        self._book_scraper = book_scraper

    @classmethod
    def _prepare_book_urls(cls, search_url: str, book_urls: list[str]) -> list[str]:
        """
        Prepare book URLs if they don't have a domain.
        """
        parsed_url = urlparse(search_url)
        protocol = parsed_url.scheme
        domain = parsed_url.netloc

        url_prefix = f"{protocol}://{domain}"

        prepared_book_urls = []
        for book_url in book_urls:
            if book_url.startswith('/'):
                book_url = url_prefix + book_url

            prepared_book_urls.append(book_url)

        return prepared_book_urls

    async def _iter_book_url_batches(self, url: str, config: dict[str, ParserFieldConfig]) -> AsyncIterator[list[str]]:
        """
        Iterate over all book urls.
        """
        page_number = 1
        while True:
            page_url = Template(url).substitute(page_number=page_number)
            async with self._scraper.get_page() as page:
                await page.goto(url=page_url)
                book_urls = await parse_config(config=config, target=page)
                if 'book_urls' not in book_urls:
                    break

                book_urls = self._prepare_book_urls(search_url=url, book_urls=book_urls['book_urls'])

            page_number += 1
            yield book_urls

    async def iter_scrape_books_batches(self) -> AsyncIterator[list[Book]]:
        """
        Run the scraper.
        """
        if self._config.new_books_url:
            async for book_url_batch in self._iter_book_url_batches(
                url=self._config.new_books_url,
                config=self._config.new_books_config or self._config.config,
            ):
                tasks = [
                    self._book_scraper.scrape(
                        url=book_url,
                        config=self._config.book_page_config,
                        incoming_status=BookStatus.NEW,
                        publisher_name=self._config.name,
                    )
                    for book_url in book_url_batch
                ]
                results = await asyncio.gather(*tasks)

                yield [result for result in results if result is not None]

        if self._config.preorder_books_url:
            async for book_url_batch in self._iter_book_url_batches(
                    url=self._config.preorder_books_url,
                    config=self._config.preorder_books_config or self._config.config,
            ):
                tasks = [
                    self._book_scraper.scrape(
                        url=book_url,
                        config=self._config.book_page_config,
                        incoming_status=BookStatus.PREORDER,
                        publisher_name=self._config.name,
                    )
                    for book_url in book_url_batch
                ]
                results = await asyncio.gather(*tasks)

                yield [result for result in results if result is not None]

        if self._config.coming_soon_books_url:
            async for book_url_batch in self._iter_book_url_batches(
                    url=self._config.coming_soon_books_url,
                    config=self._config.coming_soon_books_config or self._config.config,
            ):
                tasks = [
                    self._book_scraper.scrape(
                        url=book_url,
                        config=self._config.book_page_config,
                        incoming_status=BookStatus.COMING_SOON,
                        publisher_name=self._config.name,
                    )
                    for book_url in book_url_batch
                ]
                results = await asyncio.gather(*tasks)

                yield [result for result in results if result is not None]
