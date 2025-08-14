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
from store.store_novel_info import ChapterStore
from constant.constant import Chapterinfo

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

    async def search(self) -> None:
        """搜索小说地图，每本小说的名字及其链接

        Returns:
            dict[str, str]: _description_
        """
        # todo: 同时获取对应小说类型
        
        while True:
            self.chapters_info: list[Chapterinfo] = []
            await self.context_page.wait_for_load_state()
            current_page = await self.context_page.locator("body > div.header > span").text_content()
            print(f"正在下载{current_page}")
            

            # 使用 page.locator() 获取所有匹配的 a 标签
            chapter_locators: list[Locator] = await self.context_page.locator("body > div.wrap.rank > div > ul > li").all()
            # 或者写成 .wrap.rank li > a
            for locator in chapter_locators:
                title = await locator.locator('a').text_content()
                # 相当于 BeautifulSoup 的 get_text()
                url = self.index_url + str(await locator.locator('a').get_attribute("href"))
                # 相当于 BeautifulSoup 的 ["href"]
                chapter_type = await locator.locator('span').text_content()

                self.chapters_info.append(Chapterinfo(title=title, url=url, type=chapter_type))

            if self.chapters_info:
                await ChapterStore().save_chapterinfo(self.chapters_info)
            if await self._has_next_page():
                await self._goto_next_page(self.context_page)
            else:
                break
    async def _goto_next_page(self, page: Page) -> Optional[Page]:
        """跳转到下一页"""
        await page.click("div.page a:text('>')")

    async def _has_next_page(self) -> bool:
        """判断是否有下一页"""
        return await self.context_page.locator("div.page a:text('>')").count() > 0
    
    async def launch_browser(self, chromium: BrowserType, user_agent: Optional[str], headless: bool = True) -> BrowserContext:
        browser_context = await chromium.launch_persistent_context(
            user_data_dir="data",
            headless=headless,
            user_agent=user_agent
        )
        return browser_context

