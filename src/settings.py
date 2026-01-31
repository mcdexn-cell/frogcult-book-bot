"""
Provide settings.
"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class ScraperSettings(BaseModel):
    """
    Scraper settings.
    """
    book_batch_size: int = 10


class Settings(BaseSettings):
    """
    Settings class.
    """
    scraper: ScraperSettings = ScraperSettings()

    postgres_url: str
    bot_token: str


settings = Settings()
