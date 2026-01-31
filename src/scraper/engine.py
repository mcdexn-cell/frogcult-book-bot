"""
Provide scraping engine implementation.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from playwright.async_api import (
    async_playwright,
    Browser,
    Page,
)

from src.scraper.constants import (
    SCRAPER_VIEWPORT,
    SCRAPER_USER_AGENT,
)


class PlaywrightScraperEngine:
    def __init__(
            self,
            headless: bool = True,
            browser_type: str = "chromium",
            viewport: dict[str, int] | None = None,
            user_agent: str | None = None,
            timeout: int = 30000,
    ):
        """
        Initialize the Playwright wrapper.

        Args:
            headless: Run browser in headless mode
            browser_type: Browser type ('chromium', 'firefox', 'webkit')
            viewport: Viewport size dict with 'width' and 'height'
            user_agent: Custom user agent string
            timeout: Default timeout in milliseconds
        """
        self.headless = headless
        self.browser_type = browser_type
        self.viewport = viewport or SCRAPER_VIEWPORT
        self.user_agent = user_agent or SCRAPER_USER_AGENT
        self.timeout = timeout

        self._playwright = None
        self._browser: Browser | None = None

    async def __aenter__(self):
        """
        Async context manager entry.
        """
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit.
        """
        await self.close()

    async def start(self):
        """
        Start the browser instance.
        """
        self._playwright = await async_playwright().start()

        browser_launcher = getattr(self._playwright, self.browser_type)
        self._browser = await browser_launcher.launch(headless=self.headless)

    async def close(self):
        """
        Close the browser and cleanup resources.
        """
        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

    @asynccontextmanager
    async def get_page(self, cookies: list[dict] | None = None) -> AsyncGenerator[Page]:
        """
        Get browser page.

        Returns:
            The page instance
        """

        context = await self._browser.new_context(viewport=self.viewport, user_agent=self.user_agent)
        context.set_default_timeout(self.timeout)

        if cookies:
            await context.add_cookies(cookies)

        page = await context.new_page()

        yield page

        await page.close()
        await context.close()
