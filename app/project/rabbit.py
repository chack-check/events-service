import asyncio
import logging

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractIncomingMessage
from pydantic import ValidationError

from app.schemas import SystemEvent

from .settings import settings

logger = logging.getLogger("uvicorn.error")


class EventSubscriber:

    def __init__(self, user_id: int, event_types: list[str]):
        self.user_id = user_id
        self.event_types = event_types
        self._futures: list[asyncio.Future[list[SystemEvent]]] = []

    async def read(self) -> list[SystemEvent]:
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self._futures.append(future)
        return await future

    def set_event(self, events: list[SystemEvent]):
        for future in self._futures:
            if future.cancelled() or future.done():
                continue

            future.set_result(events)

        self._futures.clear()


class EventsPublisher:

    def __init__(self):
        self._subscribers: list[EventSubscriber] = []

    def add_subscriber(self, subscriber: EventSubscriber):
        self._subscribers.append(subscriber)

    def send(self, events: list[SystemEvent]):
        for subscriber in self._subscribers:
            subscriber_events = [event for event in events if (not event.included_users or subscriber.user_id in event.included_users) and event.event_type in subscriber.event_types]
            subscriber.set_event(subscriber_events)


class Rabbit:

    def __init__(self, exchange_names: list[str], queue_name: str):
        self._connection: AbstractConnection | None = None
        self._exchange_names = exchange_names
        self._queue_name = queue_name

        self.publisher = EventsPublisher()

    async def connect(self) -> None:
        credentials = f"{settings.rabbit_user}:{settings.rabbit_password}"
        host_and_port = f"{settings.rabbit_host}:{settings.rabbit_port}"
        self._connection = await aio_pika.connect_robust(
            f"amqp://{credentials}@{host_and_port}"
        )

    async def on_messages_received(self, messages: list[AbstractIncomingMessage]) -> None:
        system_events: list[SystemEvent] = []
        for message in messages:
            try:
                SystemEvent.model_validate_json(message.body)
            except ValidationError:
                logger.error(f"Error when decoding message from rabbitmq: {messages=}")
                continue

        logger.info(f"Received events {system_events} from rabbitmq")
        if not system_events:
            return

        self.publisher.send(system_events)
        for message in messages:
            await message.ack()

    async def listen(self):
        assert self._connection, "You need to run `connect()` method first"
        async with self._connection:
            channel = await self._connection.channel()
            await channel.set_qos(prefetch_count=10)
            queue = await channel.declare_queue(self._queue_name, durable=False)
            for exchange_name in self._exchange_names:
                exchange = await channel.declare_exchange(
                    exchange_name,
                    aio_pika.ExchangeType.FANOUT,
                    durable=True,
                )
                await queue.bind(exchange)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    if queue_iter._queue.empty():
                        await asyncio.sleep(0.15)

                    if queue_iter._queue.empty():
                        await self.on_messages_received([message])
                    else:
                        received_messages = [message]
                        while not queue_iter._queue.empty():
                            received_messages.append(await anext(queue_iter))

                        await self.on_messages_received(received_messages)


events_rabbit = Rabbit([settings.chats_exchange_name, settings.users_exchange_name], settings.queue_name)
