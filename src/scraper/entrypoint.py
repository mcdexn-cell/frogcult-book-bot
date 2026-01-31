"""
Provide scraper entrypoint.
"""
import asyncio

from src.dependencies.database import (
    get_engine,
    get_session,
)
from src.repositories.books import BooksRepository
from src.scraper.config import PUBLISHERS_CONFIG
from src.scraper.engine import PlaywrightScraperEngine
from src.utils.extractors import PhraseExtractionService
from src.utils.extractors import (
    GENRES_MAPPING,
    GENRES_NOISE_WORDS,
    PUBLISHERS_MAPPING,
)
from src.scraper.scraper import MainScraper


async def main():
    engine = PlaywrightScraperEngine()
    await engine.start()

    genre_extractor = PhraseExtractionService(phrases_mapping=GENRES_MAPPING, noise_words=GENRES_NOISE_WORDS)
    publisher_extractor = PhraseExtractionService(phrases_mapping=PUBLISHERS_MAPPING)
    books_repo = BooksRepository(session=get_session())

    scraper = MainScraper(
        books_repository=books_repo,
        scraper_engine=engine,
        book_scraper_params={
            'genre_extractor': genre_extractor,
            'publisher_extractor': publisher_extractor,
        }
    )

    try:
        await scraper.run_with_config(config=PUBLISHERS_CONFIG, handle_alerts=False)

    finally:
        await engine.close()
        await get_engine().dispose()


if __name__ == "__main__":
    asyncio.run(main())
