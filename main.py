import asyncio
from typing import Optional

from playwright.async_api import async_playwright

from novel import ChapterCrawler


crawler: Optional[ChapterCrawler] = None
async def main():
    global crawler
    crawler = ChapterCrawler()
    await crawler.start()
    with open("chapters.txt", "w", encoding="utf-8") as f:
        for chapter, url in crawler.chapters.items():
            f.write(f"{chapter, url}\n")

if __name__ == "__main__":
    asyncio.run(main())