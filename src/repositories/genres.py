"""
Genres repository class implementation.
"""

from sqlalchemy import select
from sqlalchemy.orm import load_only
from sqlalchemy.dialects.postgresql import insert

from src.database.models import Genres
from src.repositories.base import PostgresRepository
from src.structures.genres import GenreInDb


class GenresRepository(PostgresRepository):
    """
    Genres repository class implementation.
    """

    async def insert_genres(self, genres: list[GenreInDb]):
        """
        Insert genres into database.

        Args:
            genres: list of genres to insert.
        """
        stmt = insert(Genres)
        stmt = stmt.on_conflict_do_nothing()
        async with self._session() as session:
            await session.execute(stmt, [genre.model_dump(mode='json') for genre in genres])
            await session.commit()

    async def get_genre_id_to_mapping(self) -> dict[int, list[str]]:
        """
        Get genres id to publisher mapping.

        Returns:
            genres ID to publisher mapping as dict.
        """
        stmt = select(Genres).options(load_only(Genres.id, Genres.mapping))

        async with self._session() as session:
            results_raw = await session.execute(stmt)
            results = results_raw.scalars().fetchall()

        return {result.id: result.mapping for result in results}
