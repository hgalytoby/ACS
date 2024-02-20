import os

from aiopath import AsyncPath


class FileTool:
    @classmethod
    async def save(cls, path: str, file: bytes):
        path = AsyncPath(path)
        await path.parent.mkdir(exist_ok=True, parents=True)
        await path.write_bytes(file)

    @classmethod
    async def remove(cls, path: str):
        path = AsyncPath(f'{os.getcwd()}{path}')
        if await path.is_file():
            await path.unlink()
