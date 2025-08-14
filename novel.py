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
from store.store_novel_info import NovelsStore
from store.store_content import NovelStore
from model.model import Novelsinfo, NovelInfo

class NovelCrawler(AbstractNovelCrawler):
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
            self.chapters_info: list[Novelsinfo] = []
            await self.context_page.wait_for_load_state()
            current_page = await self.context_page.locator("body > div.header > span").text_content()
            print(f"正在下载{current_page}")
            

            self.chapters_info = await self.get_novels_fast()
            if self.chapters_info:
                await NovelsStore().save_chapterinfo(self.chapters_info)
            if await self._has_next_page():
                await self._goto_next_page(self.context_page)
            else:
                break

    async def get_novels_fast(self):
        all_data = await self.context_page.locator("body > div.wrap.rank > div > ul > li").evaluate_all("""
        (listItems, baseurl) => listItems.map(item => {
            const a = item.querySelector('a');
            const span = item.querySelector('span');
            return {
                title: a.textContent.trim(),
                url: baseurl + a.getAttribute('href'),
                type: span.textContent.trim()
            };
        })
        """
        , self.index_url)
        return [Novelsinfo(**data) for data in all_data]
    async def _goto_next_page(self, page: Page):
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


class ChapterCrawler(NovelCrawler):
    def __init__(self, index_url) -> None:
        super().__init__()
        self.index_url = index_url

    async def start(self):
        async with async_playwright() as p:
            self.browser_context = await self.launch_browser(p.chromium, self.user_agent, headless=False)
            await self.browser_context.add_init_script(path="libs/stealth.min.js")
            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(self.index_url)
            await self.get_meta_data()
            await self.search()
    
    async def get_meta_data(self):
        await self.context_page.wait_for_load_state()
        title = await self.context_page.locator(".name").text_content()
        author = await self.context_page.locator("body > div.books > div.book_info > div.book_box > dl > dd:nth-child(2) > span:nth-child(1)").text_content()
        intro = await self.context_page.locator("body > div.books > div.book_about > dl > dd").text_content()
        type = await self.context_page.locator("body > div.books > div.book_info > div.book_box > dl > dd:nth-child(2) > span:nth-child(2)").text_content()
        wordsount = await self.context_page.locator("body > div.books > div.book_info > div.book_box > dl > dd:nth-child(3) > span:nth-child(2)").text_content()
        updatetime = await self.context_page.locator("body > div.books > div.book_info > div.book_box > dl > dd:nth-child(4) > span").text_content()
        status = await self.context_page.locator("body > div.books > div.book_info > div.book_box > dl > dd:nth-child(3) > span:nth-child(1)").text_content()
        
        self.meta_data: NovelInfo = NovelInfo(title=title, author=author, intro=intro, type=type, wordsount=wordsount, last_update=updatetime, status=status, index_url=self.index_url)
    async def search(self):
        await self.context_page.locator("body > div.books > div.book_more > a").click()
        await self.context_page.wait_for_load_state()
        await self.context_page.locator("body > div.book_last > dl > dd:nth-child(3) > a").click()
        await self.context_page.wait_for_load_state()
        while True:
            chapter_name = await self.context_page.locator("#read > div.header > span").text_content()
            print(f"正在下载章节: {chapter_name}")
            content = await self.context_page.locator("#chaptercontent").text_content()
            await NovelStore(self.meta_data.title).save_chapter(content)
            if await self._has_next_page():
                await self._goto_next_page(self.context_page)
            else:
                break
            
    async def _goto_next_page(self, page):
        return await page.click("#pb_next")
    
    async def _has_next_page(self):
        return await self.context_page.locator("#pb_next").count() > 0
    async def launch_browser(self, chromium: BrowserType, user_agent: Optional[str], headless: bool = True) -> BrowserContext:
        browser_context = await chromium.launch_persistent_context(
            user_data_dir="data",
            headless=headless,
            user_agent=user_agent
        )
        return browser_context