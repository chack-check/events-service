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
    message_deleted = "message_deleted"
    message_reaction_deleted = "message_reaction_deleted"
    message_updated = "message_updated"


@strawberry.enum
class ChatEventTypesEnum(Enum):
    chat_created = "chat_created"
    chat_deleted = "chat_deleted"


@strawberry.enum
class UserEventTypesEnum(Enum):
    user_created = "user_created"
    user_changed = "user_changed"


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
class UserAvatar:
    original_url: str
    original_filename: str
    converted_url: str | None = None
    converted_filename: str | None = None


@strawberry.type
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email_confirmed: bool
    phone_confirmed: bool
    avatar: UserAvatar
    last_seen: datetime | None
    status: str | None = None
    middle_name: str | None = None
    phone: str | None = None
    email: str | None = None


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


@strawberry.type
class UserEvent:
    event_type: UserEventTypesEnum
    included_users: list[int]
    user: User
