"""
Provide scraper entrypoint.
"""
import asyncio

from src.dependencies.database import (
    get_engine,
    get_session,
)
from src.dependencies.repositories import get_genres_repository, get_publishers_repository
from src.repositories.books import BooksRepository
from src.scraper.config import PUBLISHERS_CONFIG
from src.scraper.engine import PlaywrightScraperEngine
from src.utils.extractors.service import PhraseExtractionService
from src.utils.extractors.mappings import GENRES_NOISE_WORDS
from src.scraper.scraper import MainScraper


async def main():
    engine = PlaywrightScraperEngine()
    await engine.start()

    genres_repo = get_genres_repository()
    publishers_repo = get_publishers_repository()

    genres_mapping = await genres_repo.get_genre_id_to_mapping()
    publishers_mapping = await publishers_repo.get_publisher_id_to_mapping()

    genre_extractor = PhraseExtractionService(phrases_mapping=genres_mapping, noise_words=GENRES_NOISE_WORDS)
    publisher_extractor = PhraseExtractionService(phrases_mapping=publishers_mapping)
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
