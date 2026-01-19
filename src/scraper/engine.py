"""
Provide scraping engine implementation.
"""

from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
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
        self._context: BrowserContext | None = None
        self._page: Page | None = None

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

        self._context = await self._browser.new_context(viewport=self.viewport, user_agent=self.user_agent)
        self._context.set_default_timeout(self.timeout)

        self._page = await self._context.new_page()

    async def close(self):
        """
        Close the browser and cleanup resources.
        """
        if self._page:
            await self._page.close()

        if self._context:
            await self._context.close()

        if self._browser:
            await self._browser.close()

        if self._playwright:
            await self._playwright.stop()

    @property
    def page(self) -> Page:
        """
        Get the current page instance.
        """
        if not self._page:
            raise RuntimeError("Browser not started. Call start() or use context manager.")

        return self._page

    @property
    def context(self) -> BrowserContext:
        """
        Get the browser context.
        """
        if not self._context:
            raise RuntimeError("Browser not started. Call start() or use context manager.")

        return self._context

    async def goto(
            self,
            url: str,
            wait_until: str = 'domcontentloaded',
            timeout: int | None = None,
    ) -> Page:
        """
        Navigate to a URL.

        Args:
            url: The URL to navigate to
            wait_until: When to consider navigation succeeded ('load', 'domcontentloaded', 'networkidle', 'commit')
            timeout: Navigation timeout in milliseconds

        Returns:
            The page instance
        """
        await self.page.goto(url, wait_until=wait_until, timeout=timeout)

        return self.page
