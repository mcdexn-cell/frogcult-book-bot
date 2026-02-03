"""
Provide models for database.
"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    create_engine,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from src.enums.book import BookStatus


class Base(DeclarativeBase):
    """
    Abstract table declarative base class.
    """


class Books(Base):
    """
    Books table.
    """
    __tablename__ = "books"

    isbn: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    url: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    publisher_id: Mapped[int] = mapped_column(Integer, nullable=True)
    publisher: Mapped[str] = mapped_column(String)
    genres: Mapped[dict] = mapped_column(JSON, nullable=True)
    status: Mapped[BookStatus] = mapped_column(Enum(BookStatus))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.utcnow, nullable=True)


class BookAlerts(Base):
    """
    Alerts table.
    """
    __tablename__ = "book_alerts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    isbn: Mapped[int] = mapped_column(BigInteger, ForeignKey(Books.isbn))
    status_before: Mapped[BookStatus] = mapped_column(Enum(BookStatus), nullable=True)
    status_after: Mapped[BookStatus] = mapped_column(Enum(BookStatus), nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Users(Base):
    """
    Users table.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    subscribed_genres: Mapped[list] = mapped_column(JSON, nullable=True)
    subscribed_publishers: Mapped[list] = mapped_column(JSON, nullable=True)
    subscribed_authors: Mapped[list] = mapped_column(JSON, nullable=True)


class Publishers(Base):
    """
    Publishers table.
    """
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    mapping: Mapped[dict] = mapped_column(JSON)


class Genres(Base):
    """
    Genres table.
    """
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    mapping: Mapped[dict] = mapped_column(JSON)


class BookGenres(Base):
    """
    Book genres table.
    """
    __tablename__ = "book_genres"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    book_isbn: Mapped[int] = mapped_column(BigInteger, ForeignKey(Books.isbn))
    genre_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Genres.id))


engine = create_engine('postgresql+psycopg2://test:test@127.0.0.1:5432/test')
Base.metadata.create_all(engine)
