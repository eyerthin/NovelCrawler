from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    """
    Abstract class for all crawlers
    """
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def start(self):
        """
        Get data from url
        """
        pass

    @abstractmethod
    def search(self):
        """
        Get data from url
        """
        pass