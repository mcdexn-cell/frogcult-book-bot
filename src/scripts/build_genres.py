"""
Build genres for the table insert.
"""
import asyncio

from src.dependencies.database import get_engine
from src.dependencies.repositories import get_genres_repository
from src.enums.book import (
    GENRE_TO_CATEGORY_MAP,
)
from src.structures.genre import GenreInDb
from src.utils.extractors.mappings import GENRES_MAPPING


def build_from_constants() -> list[GenreInDb]:
    return [
        GenreInDb(id=i + 1, name=genre, category=GENRE_TO_CATEGORY_MAP[genre], mapping=mapping)
        for i, (genre, mapping) in enumerate(GENRES_MAPPING.items())
    ]

async def main():
    res = build_from_constants()

    repository = get_genres_repository()

    await repository.insert_genres(res)
    await get_engine().dispose()


if __name__ == "__main__":
    asyncio.run(main())
