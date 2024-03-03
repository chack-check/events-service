import asyncio
import logging

import aio_pika

from app.schemas import SystemEvent

from .settings import settings

logger = logging.getLogger(__file__)


class EventSubscriber:

    def __init__(self, user_id: int, event_types: list[str]):
        self.user_id = user_id
        self.event_types = event_types
        self._futures: list[asyncio.Future[SystemEvent]] = []

    async def read(self) -> SystemEvent:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._futures.append(future)
        return await future

    def set_event(self, event: SystemEvent):
        for future in self._futures:
            if future.cancelled() or future.done():
                continue

            future.set_result(event)

        self._futures.clear()


class EventsPublisher:

    def __init__(self):
        self._subscribers: list[EventSubscriber] = []

    def add_subscriber(self, subscriber: EventSubscriber):
        self._subscribers.append(subscriber)

    def send(self, event: SystemEvent):
        for subscriber in self._subscribers:
            assert subscriber.user_id in event.included_users, (f"{subscriber.user_id=}", f"{event=}")
            assert event.event_type in subscriber.event_types, (f"{subscriber.event_type=}", f"{event=}")
            if subscriber.user_id in event.included_users and event.event_type in subscriber.event_types:
                subscriber.set_event(event)


class Rabbit:

    def __init__(self, exchange_name: str, queue_name: str):
        self._connection: aio_pika.Connection | None = None
        self._exchange_name = exchange_name
        self._queue_name = queue_name

        self.publisher = EventsPublisher()

    async def connect(self) -> None:
        credentials = f"{settings.rabbit_user}:{settings.rabbit_password}"
        host_and_port = f"{settings.rabbit_host}:{settings.rabbit_port}"
        self._connection = await aio_pika.connect_robust(
            f"amqp://{credentials}@{host_and_port}"
        )

    async def on_message_received(self, message: aio_pika.IncomingMessage) -> None:
        try:
            system_event = SystemEvent.model_validate_json(message.body)
        except Exception as e:
            logger.error(f"Error when decoding rabbitmq message: {e}")
            return

        logger.info(f"Received event {system_event} from rabbitmq")
        self.publisher.send(system_event)
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


events_rabbit = Rabbit(settings.chats_exchange_name, settings.queue_name)
