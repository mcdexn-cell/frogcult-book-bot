"""
Publishers repository class implementation.
"""

from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Publishers
from src.repositories.base import PostgresRepository
from src.structures.publisher import PublisherInDb


class PublishersRepository(PostgresRepository):
    """
    Publishers repository class implementation.
    """

    async def insert_publishers(self, publishers: list[PublisherInDb]):
        """
        Insert publishers into database.

        Args:
            publishers: list of publishers to insert.
        """
        stmt = insert(Publishers)
        stmt = stmt.on_conflict_do_nothing()
        async with self._session() as session:
            await session.execute(stmt, [publisher.model_dump(mode='json') for publisher in publishers])
            await session.commit()

    async def get_publishers_by_ids(self, ids: list[int]) -> list[PublisherInDb]:
        """
        Get publishers data by ids.

        Args:
            ids: list of publisher ids.

        Returns:
            list of publishers data.
        """
        stmt = select(Publishers).where(Publishers.id.in_(ids))
        async with self._session() as session:
            results = (await session.execute(stmt)).scalars().all()

            return [
                PublisherInDb(id=result.id, name=result.name, mapping=result.mapping)
                for result in results
            ]

    async def get_publisher_id_to_mapping(self) -> dict[int, list[str]]:
        """
        Get publisher id to publisher mapping.

        Returns:
            publisher ID to publisher mapping as dict.
        """
        stmt = select(Publishers).options(load_only(Publishers.id, Publishers.mapping))

        async with self._session() as session:
            results_raw = await session.execute(stmt)
            results = results_raw.scalars().fetchall()

        return {result.id: result.mapping for result in results}
