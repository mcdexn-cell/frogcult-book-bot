"""
Provide base book scraper implementation.
"""
import asyncio

from src.enums.book import BookStatus
from src.scraper.engine import PlaywrightScraperEngine
from src.utils.extractors.service import PhraseExtractionService
from src.scraper.utils import parse_config
from src.structures.book import Book
from src.structures.scraper import ParserFieldConfig


REQUIRED_FIELDS = ['isbn', 'title', 'author', 'genres']


class BaseBookScraper:
    """
    Provide base book scraper implementation.
    """
    def __init__(
        self,
        scraper_engine: PlaywrightScraperEngine,
        genre_extractor: PhraseExtractionService,
        publisher_extractor: PhraseExtractionService,
        semaphore: asyncio.Semaphore | None = None,
    ):
        """
        Construct the object.
        """
        self._semaphore = semaphore or asyncio.Semaphore(20)
        self._scraper = scraper_engine
        self._genre_extractor = genre_extractor
        self._publisher_extractor = publisher_extractor

    async def scrape(
        self,
        url: str,
        config: dict[str, ParserFieldConfig],
        incoming_status: str,
        publisher_name: str,
    ) -> Book | None:
        """
        Scrape book single page.
        """
        async with self._semaphore:
            async with self._scraper.get_page() as page:
                await page.goto(url=url)
                print(url)
                parsed_results = await parse_config(config=config, target=page)
                print(parsed_results)

                for field in REQUIRED_FIELDS:
                    if field not in parsed_results:
                        return None

                publisher = parsed_results.get('publisher', publisher_name)
                publisher_ids = self._publisher_extractor.extract_phrases(publisher)

                result = Book(
                    url=url,
                    title=parsed_results['title'],
                    author=parsed_results['author'],
                    source=publisher_name,
                    publisher=publisher,
                    publisher_id=publisher_ids[0] if publisher_ids else None,
                    status=BookStatus(parsed_results.get('status', incoming_status)),
                    isbn=self._normalize_isbn(isbn=parsed_results['isbn']),
                    genre_ids=self._extract_genres(parsed_results['genres'].split(',')),
                    genres_raw=parsed_results['genres'].split(','),
                )

        return result

    @classmethod
    def _normalize_isbn(cls , isbn: str) -> int:
        """
        Normalize isbn.
        """
        return int(isbn.replace('-', ''))

    def _extract_genres(self, parsed_genres: list[str]) -> list[int]:
        """
        Extract genres from parsed.
        """
        genres = []
        for raw_genre in parsed_genres:
            extracted = self._genre_extractor.extract_phrases(text=raw_genre)
            genres.extend(extracted)

        return genres
