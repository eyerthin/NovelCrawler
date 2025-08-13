from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple
import logging
import asyncio

from playwright.sync_api import Page, Browser, async_playwright


class AbstractNovelCrawler(ABC):
    """
    Abstract class for all crawlers
    """
    def __init__(self, base_url: str):
        self.url = base_url
        self.novel_metadata = {
            "author": None,
            "index_href": None,
            "title": None,
            "description": None,
            "content": []
        }
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def _fetch_html_content(self, page: Page, url: str) -> Optional[str]:
        """
        抽象方法：使用Playwright获取HTML内容
        """
        pass

    @abstractmethod
    async def _extract_novel_metadata(self, page: Page) -> Dict:
        """
        抽象方法：从目录页提取小说元数据
        """
        pass

    @abstractmethod
    async def _parse_chapter_list(self, page: Page) -> list[Tuple[str, str]]:
        """
        抽象方法：从目录页解析章节列表
        返回（章节名，章节URL）列表
        """
        pass

    @abstractmethod
    async def _parse_chapter_content(self, page: Page) -> str:
        """
        抽象方法：从章节页解析章节内容
        返回章节内容
        """
        pass

    async def _download_chapter(self, page: Page, chapter_name: str, chapter_url: str) -> Optional[Dict]:
        """
        下载章节内容
        """
        try:
            await self._fetch_html_content(page, chapter_url)
            content = await self._parse_chapter_content(page)
            if content:
                self.logger.info(f"已下载章节：{chapter_name}")
                return {chapter_name: content}
            else:
                self.logger.error(f"下载章节失败：{chapter_name}")
                return None
        except Exception as e:
            self.logger.error(f"下载章节内容失败：{e}")
            return None
        
    async def scrape(self, index_url: str, max_chapters: int = 20) -> bool:
        """ 
        核心爬虫逻辑
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            self.logger.info(f"正在访问小说目录页：{self.url}")
            await self._fetch_html_content(page, index_url)

            self.novel_metadata["index_href"] = index_url
            metadata = await self.get_novel_metadata(page)
            self.novel_metadata.update(metadata)

            chapter_list = await self._parse_chapter_list(page)

            if not chapter_list:
                self.logger.error("没有找到章节列表")
                await browser.close()
                return False
            
            self.logger.info(f"找到 {len(chapter_list)} 章节")

            tasks = []
            for name, href in chapter_list[:max_chapters]:
                tasks.append(self._download_chapter(page.context.new_page(), name, href))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, dict):
                    self.novel_metadata["content"].append(result)
            
            self.logger.info("所有章节下载完成，成功下载{len(self.novel_metadata['content'])}个章节")

            await self.browser.close()
            return True