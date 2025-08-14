import asyncio
from typing import Optional

from playwright.async_api import async_playwright

from novel import NovelCrawler


crawler: Optional[NovelCrawler] = None
async def main():
    global crawler
    crawler = NovelCrawler()
    await crawler.start()

if __name__ == "__main__":
    asyncio.run(main())