import msgspec
import aio_pika

from .settings import settings
from ..ws_pool import ws_pool, ConnectionsPool


class Rabbit:

    def __init__(self, queue_name: str, ws_pool: ConnectionsPool):
        self._connection: aio_pika.Connection | None = None
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
        await ws_pool.send(message_json['includedUsers'], message_json)
        await message.ack()

    async def listen(self):
        assert self._connection, "You need to run `connect()` method first"
        async with self._connection:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(self._queue_name)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    await self.on_message_received(message)


events_rabbit = Rabbit(settings.rabbit_events_queue_name, ws_pool)
