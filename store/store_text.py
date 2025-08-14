import aiofiles

from base import AbstractStore

class ChapterStore(AbstractStore):
    save_path: str = "save_data/chapter.txt"

    async def save_dict_to_txt(self, save_item: dict):
        async with aiofiles.open(self.save_path, mode='a+', encoding='utf-8') as f:
            f.fileno()
            if await f.tell() == 0:
                for key, value in save_item.items():
                    await f.write(f"{key},{value}\n")

    async def store(self):
        pass