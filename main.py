import asyncio
from typing import Optional

from playwright.async_api import async_playwright

from novel import ChapterCrawler


crawler: Optional[ChapterCrawler] = None
async def main():
    global crawler
    crawler = ChapterCrawler()
    await crawler.start()

if __name__ == "__main__":
    asyncio.run(main())