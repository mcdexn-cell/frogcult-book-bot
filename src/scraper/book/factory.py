"""
Provide book scraper factory.
"""
from asyncio import Semaphore

from src.scraper.book.base import BaseBookScraper
from src.scraper.engine import PlaywrightScraperEngine
from src.utils.extractors import PhraseExtractionService


class BookScraperFactory:
    """
    Publisher factory class.
    """
    publisher_name_to_scraper_map: dict[str, BaseBookScraper] = {}

    @classmethod
    def get(
        cls,
        publisher_name: str,
        *,
        scraper_engine: PlaywrightScraperEngine,
        genre_extractor: PhraseExtractionService,
        publisher_extractor: PhraseExtractionService,
        semaphore: Semaphore | None = None,
    ) -> BaseBookScraper:
        """
        Get book scraper instance.
        """
        book_scraper_class = cls.publisher_name_to_scraper_map.get(publisher_name, BaseBookScraper)

        return book_scraper_class(
            scraper_engine=scraper_engine,
            genre_extractor=genre_extractor,
            publisher_extractor=publisher_extractor,
            semaphore=semaphore,
        )
