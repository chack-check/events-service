import logging

import aio_pika
import msgspec

from ..ws_pool import ConnectionsPool, ws_pool
from .settings import settings

logger = logging.getLogger(__file__)


class Rabbit:

    def __init__(self, exchange_name: str, queue_name: str, ws_pool: ConnectionsPool):
        self._connection: aio_pika.Connection | None = None
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._ws_pool = ws_pool

    async def connect(self) -> None:
        credentials = f"{settings.rabbit_user}:{settings.rabbit_password}"
        host_and_port = f"{settings.rabbit_host}:{settings.rabbit_port}"
        self._connection = await aio_pika.connect_robust(
            f"amqp://{credentials}@{host_and_port}"
        )

    async def on_message_received(self, message: aio_pika.IncomingMessage) -> None:
        message_json = msgspec.json.decode(message.body)
        logger.error(message_json)
        print(message_json)
        if not message_json.get('includedUsers'):
            return

        await ws_pool.send(message_json['includedUsers'], message_json)
        await message.ack()

    async def listen(self):
        assert self._connection, "You need to run `connect()` method first"
        async with self._connection:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(self._queue_name, durable=True)
            exchange = await channel.declare_exchange(
                self._exchange_name,
                aio_pika.ExchangeType.FANOUT,
                durable=True,
            )
            await queue.bind(exchange)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await self.on_message_received(message)


events_rabbit = Rabbit(settings.chats_exchange_name, settings.queue_name, ws_pool)
