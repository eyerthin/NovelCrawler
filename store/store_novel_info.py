import aiofiles

from base import AbstractStore
from model.model import Novelsinfo

class NovelsStore(AbstractStore):
    save_path: str = "save_data/chapter.txt"

    async def save_dict_to_txt(self, save_item: dict):
        async with aiofiles.open(self.save_path, mode='a+', encoding='utf-8') as f:
            f.fileno()
            if await f.tell() == 0:
                for key, value in save_item.items():
                    await f.write(f"{key},{value}\n")

    async def save_chapterinfo(self, chapterinfos: list[Novelsinfo]):
        async with aiofiles.open(self.save_path, mode='a+', encoding='utf-8') as f:
            f.fileno()
            if await f.tell() == 0:
                await f.write("title,url,type\n")
            for chapterinfo in chapterinfos:
                await f.write(f"{chapterinfo.title},{chapterinfo.url},{chapterinfo.type}\n")
    async def store(self):
        pass