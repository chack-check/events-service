from datetime import datetime
from enum import Enum

import strawberry


@strawberry.enum
class MessageTypesEnum(Enum):
    text = "text"
    event = "event"
    call = "call"
    voice = "voice"
    circle = "circle"


@strawberry.enum
class MessageEventTypesEnum(Enum):
    message_created = "message_created"
    message_readed = "message_readed"
    message_reacted = "message_reacted"


@strawberry.enum
class ChatEventTypesEnum(Enum):
    chat_created = "chat_created"


@strawberry.type
class Reaction:
    id: int
    user_id: int
    content: str


@strawberry.type
class Message:
    id: int
    chat_id: int
    sender_id: int
    type: MessageTypesEnum
    content: str
    voice_url: str
    circle_url: str
    attachments: list[str]
    reply_to_id: int
    mentioned: list[int]
    readed_by: list[int]
    reactions: list[Reaction]
    datetime: datetime


@strawberry.type
class Chat:
    id: int
    avatar_url: str
    title: str
    type: str
    members: list[int]
    is_archived: bool
    owner_id: int
    admins: list[int]


@strawberry.type
class MessageEvent:
    event_type: MessageEventTypesEnum
    included_users: list[int]
    message: Message


@strawberry.type
class ChatEvent:
    event_type: ChatEventTypesEnum
    included_users: list[int]
    chat: Chat
