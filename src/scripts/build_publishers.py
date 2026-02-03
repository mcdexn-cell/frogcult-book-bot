"""
Provide publishers builder for the table insert.
"""
import asyncio

from src.dependencies.database import get_engine
from src.dependencies.repositories import get_publishers_repository
from src.structures.publishers import PublisherInDb
from src.utils.extractors.mappings import PUBLISHERS_MAPPING


def build_from_constants() -> list[PublisherInDb]:
    """
    Build publishers from constants.
    """
    return [
        PublisherInDb(id=i + 1, name=publisher, mapping=mapping)
        for i, (publisher, mapping) in enumerate(PUBLISHERS_MAPPING.items())
    ]


async def main():
    res = build_from_constants()

    repository = get_publishers_repository()

    await repository.insert_publishers(res)
    await get_engine().dispose()


if __name__ == "__main__":
    asyncio.run(main())
