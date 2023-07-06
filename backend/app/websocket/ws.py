import asyncio
import orjson
import time
from broadcaster import Broadcast
from fastapi import APIRouter
from starlette.websockets import WebSocket
from starlette.concurrency import run_until_first_complete
from fastapi_async_sqlalchemy import db

from app.core.config import settings, logger
from app.crud import crud_member_status
from app.schemas.member import MemberStatusCreatedRead
from app.schemas.websocket import WebSocketEventSchema
from app.utils.enums import WebSocketEvent

router = APIRouter()


class MyBroadcast(Broadcast):
    async def connect(self) -> None:
        logger.info('連線 Redis!!，請確認有沒有啟用 Redis!!')
        await super(MyBroadcast, self).connect()
        logger.info('連線 Redis 成功!')


broadcast = MyBroadcast(settings.redis.url)


class Client:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.accept = False

    async def login(self):
        if not self.accept:
            self.accept = True
            data = WebSocketEventSchema(
                event=WebSocketEvent.LOGIN,
                data={'success': True},
            ).json()
            await self.websocket.send_text(data=data)

    async def member_come_list(self):
        items = await crud_member_status.get_multi()
        data = WebSocketEventSchema(
            event=WebSocketEvent.MEMBER_STATUS_LIST,
            data=items,
        ).json()
        await self.websocket.send_text(data=data)

    async def member_come(self, msg: WebSocketEventSchema[MemberStatusCreatedRead]):
        data = WebSocketEventSchema(
            event=WebSocketEvent.MEMBER_STATUS,
            data=msg.data,
        ).json()
        await self.websocket.send_text(data=data)

    async def handler_message(self, message: str):
        try:
            msg = WebSocketEventSchema(**orjson.loads(message))
            match msg.event:
                case WebSocketEvent.LOGIN:
                    await self.login()
                case WebSocketEvent.MEMBER_STATUS_LIST:
                    await self.member_come_list()
                case WebSocketEvent.MEMBER_STATUS:
                    await self.member_come(msg=msg)
                case _:
                    await self.websocket.send_text('{"data":"EventError"}')
                    await self.disconnect()
        except orjson.JSONDecodeError:
            await self.websocket.send_text('{"data":"JSONDecodeError"}')
            await self.disconnect()

    async def disconnect(self):
        ...

    async def receiver(self):
        async for message in self.websocket.iter_text():
            await self.handler_message(message=message)

    async def sender(self):
        start_time = time.time()
        while not self.accept:
            if time.time() - start_time > 5:
                await self.websocket.close()
            await asyncio.sleep(1)
        async with broadcast.subscribe(channel=settings.project) as subscriber:
            async for event in subscriber:
                await self.handler_message(message=event.message)


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    async with db():
        await websocket.accept()
        client = Client(websocket=websocket)
        await run_until_first_complete(
            (client.receiver, {}),
            (client.sender, {}),
        )