import asyncio

from app.db.init_db import init_db
from app.db.session import async_session_maker


async def create_init_data() -> None:
    async with async_session_maker() as session:
        await init_db(session)


async def main() -> None:
    await create_init_data()


if __name__ == '__main__':
    asyncio.run(main())
