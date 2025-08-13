from abc import ABC, abstractmethod
from typing import Optional, Dict, Tuple
import logging
import asyncio

from playwright.sync_api import Page, Browser, BrowserType, BrowserContext


class AbstractNovelCrawler(ABC):
    """
    Abstract class for all crawlers
    """

    @abstractmethod
    async def start(self):
        """
        start crawling
        """
    @abstractmethod
    async def search(self):
        """
        search
        """
    @abstractmethod
    async def launch_browser(self, chromium: BrowserType, user_agent: Optional[str], headless: bool = True) -> BrowserContext:
        """launch browser

        Args:
            chromium (BrowserType): _description_
            user_agent (Optional[str]): _description_
            headless (bool, optional): _description_. Defaults to True.

        Returns:
            BrowserContext: _description_
        """

class AbstractStore(ABC):
    """AbstractStore

    Args:
        ABC (ABC): _description_
    """

    @abstractmethod
    async def store():
        """store

        Returns:
            _type_: _description_
        """
        pass

