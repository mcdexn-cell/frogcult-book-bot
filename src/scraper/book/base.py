"""
Provide base book scraper implementation.
"""
from src.enums.book import BookStatus
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.utils import parse_config
from src.structures.book import Book
from src.structures.scraper import ParserFieldConfig


class BaseBookScraper:
    """
    Provide base book scraper implementation.
    """
    @classmethod
    async def scrape(
        cls,
        url: str,
        config: dict[str, ParserFieldConfig],
        incoming_status: str,
        publisher_name: str,
    ):
        """
        Scrape book single page.
        """
        async with PlaywrightScraperEngine() as scraper:
            page = await scraper.goto(url=url)

            parsed_results = await parse_config(config=config, target=page)

        result = Book(
            url=url,
            title=parsed_results['title'],
            author=parsed_results['author'],
            publisher=parsed_results.get('publisher', publisher_name),
            status=BookStatus(parsed_results.get('status', incoming_status)),
            isbn=cls._normalize_isbn(isbn=parsed_results['isbn']),
            genres=parsed_results['genres'].split(','),
        )
        return result

    @classmethod
    def _normalize_isbn(cls , isbn: str) -> int:
        """
        Normalize isbn.
        """
        return int(isbn.replace('-', ''))
