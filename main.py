import asyncio
from typing import Optional

from playwright.async_api import async_playwright

from novel import NovelCrawler, ChapterCrawler


crawler: Optional[NovelCrawler] = None
async def main():
    global crawler
    # crawler = NovelCrawler()
    # await crawler.start()
    await ChapterCrawler("https://m.6978ae.lol/book/261083/").start()

if __name__ == "__main__":
    asyncio.run(main())