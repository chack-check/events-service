import logging
from typing import AsyncGenerator

import strawberry

from app.factories import ChatEventFactory, MessageEventFactory
from app.gql.types import ChatEvent, MessageEvent
from app.project.rabbit import EventSubscriber, events_rabbit
from app.services.identification import get_token_user_id

logger = logging.getLogger(__file__)


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def message_events(self, token: str) -> AsyncGenerator[MessageEvent, None]:
        user_id = get_token_user_id(token)
        subscriber = EventSubscriber(user_id, ["message_created", "message_reacted", "message_readed"])
        events_rabbit.publisher.add_subscriber(subscriber)
        while True:
            logger.info("Reading messages")
            event = await subscriber.read()
            logger.info(event)
            yield MessageEventFactory.message_event_from_system_event(event)

    @strawberry.subscription
    async def chat_events(self, token: str) -> AsyncGenerator[ChatEvent, None]:
        user_id = get_token_user_id(token)
        subscriber = EventSubscriber(user_id, ["chat_created"])
        events_rabbit.publisher.add_subscriber(subscriber)
        while True:
            logger.info("Reading messages")
            event = await subscriber.read()
            logger.info(event)
            yield ChatEventFactory.chat_event_from_system_event(event)


schema = strawberry.Schema(Query, subscription=Subscription)
