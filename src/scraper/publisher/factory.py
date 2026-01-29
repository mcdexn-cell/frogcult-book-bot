"""
Provide publisher factory.
"""
from src.scraper.book.base import BaseBookScraper
from src.scraper.config import PublisherConfig
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.publisher.base import BasePublisherScraper


class PublisherScraperFactory:
    """
    Publisher factory class.
    """
    publisher_name_to_scraper_map: dict[str, BasePublisherScraper] = {}

    @classmethod
    def get(
        cls,
        publisher_name: str,
        *,
        config: PublisherConfig,
        book_scraper: BaseBookScraper,
        scraper_engine: PlaywrightScraperEngine,
    ) -> BasePublisherScraper:
        """
        Get publisher scraper instance.
        """
        publisher_scraper_class = cls.publisher_name_to_scraper_map.get(publisher_name, BasePublisherScraper)

        return publisher_scraper_class(config=config, book_scraper=book_scraper, scraper_engine=scraper_engine)
