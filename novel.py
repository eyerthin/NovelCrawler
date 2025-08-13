from typing import Optional

from playwright.async_api import (
    async_playwright,
    Page,
    Browser,
    BrowserType,
    BrowserContext,
    Playwright,
    Locator
)

from base import AbstractNovelCrawler

class ChapterCrawler(AbstractNovelCrawler):
    context_page: Page
    browser_context: BrowserContext

    def __init__(self) -> None:
        self.index_url = "https://m.bqgl.cc/map/"
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    async def start(self):
        async with async_playwright() as p:
            self.browser_context = await self.launch_browser(p.chromium, self.user_agent)
            await self.browser_context.add_init_script(path="libs/stealth.min.js")
            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(self.index_url)
            await self.search()

    async def search(self) -> dict[str, str]:
        """搜索小说地图，每本小说的名字及其链接

        Returns:
            dict[str, str]: _description_
        """
        # todo: 同时获取对应小说类型
        await self.context_page.wait_for_selector("body > div.header > span")
       
        # 使用 page.locator() 获取所有匹配的 a 标签
        chapter_locators: list[Locator] = await self.context_page.locator("body > div.wrap.rank > div > ul > li > a").all()
        # 或者写成 .wrap.rank li > a
        
        self.chapters = {}
        for locator in chapter_locators:
            title = await locator.text_content()
            # 相当于 BeautifulSoup 的 get_text()
            url = await locator.get_attribute("href")
            # 相当于 BeautifulSoup 的 ["href"]

            self.chapters.update({title: url})
        return self.chapters
    
    async def launch_browser(self, chromium: BrowserType, user_agent: Optional[str], headless: bool = True) -> BrowserContext:
        browser_context = await chromium.launch_persistent_context(
            user_data_dir="data",
            headless=headless,
            user_agent=user_agent
        )
        return browser_context

