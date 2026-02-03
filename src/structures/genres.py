from pydantic import BaseModel

from src.enums.book import BookGenre, BookGenreCategory


class GenreInDb(BaseModel):
    id: int
    name: BookGenre
    category: BookGenreCategory
    mapping: list[str]
