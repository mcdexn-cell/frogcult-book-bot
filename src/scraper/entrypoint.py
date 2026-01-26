"""
Provide scraper entrypoint.
"""
import asyncio

from src.scraper.book.base import BaseBookScraper
from src.scraper.config import PUBLISHERS_CONFIG
from src.scraper.engine import PlaywrightScraperEngine
from src.scraper.extractors.service import PhraseExtractionService
from src.scraper.extractors.mappings import (
    GENRES_MAPPING,
    GENRES_NOISE_WORDS,
)
from src.scraper.publisher.base import BasePublisherScraper


async def main():
    engine = PlaywrightScraperEngine()
    await engine.start()

    genre_extractor = PhraseExtractionService(phrases_mapping=GENRES_MAPPING, noise_words=GENRES_NOISE_WORDS)

    try:
        publisher = BasePublisherScraper(
            config=PUBLISHERS_CONFIG[0],
            book_scraper=BaseBookScraper(scraper=engine, genre_extractor=genre_extractor),
            scraper=engine
        )
        async for url_batch in publisher.iter_scrape_books_batches():
            print(url_batch)

    finally:
        await engine.close()

if __name__ == "__main__":
    asyncio.run(main())
