import aiofiles

from base import AbstractStore

class NovelStore(AbstractStore):

    def __init__(self, save_path: str):
        self.save_path = 'save_data/' + save_path + '.txt'

    async def save_chapter(self, content):
        async with aiofiles.open(self.save_path, mode='a', encoding='utf-8') as f:
            await f.write(f"{content}\n")

    async def store(self):
        pass