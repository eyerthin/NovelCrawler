from playwright.async_api import (
    async_playwright,
    Page,
    Browser,
    BrowserContext,
    Playwright
)

from base import BaseCrawler

class NovelCrawler(BaseCrawler):
    context_page: Page
    browser_context: BrowserContext

    def __init__(self) -> None:
        self.index_url = "https://m.bqgl.cc/map/"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        
    async def start(self):
        async with async_playwright() as p:
            await self.browser_context.add_init_script(path="libs/stealth.min.js")
            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(self.index_url)

    async def search(self) -> list:
        