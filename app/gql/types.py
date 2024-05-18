from datetime import datetime
from enum import Enum

import strawberry


@strawberry.type
class SavedFile:
    original_url: str
    original_filename: str
    converted_url: str | None = None
    converted_filename: str | None = None


@strawberry.enum
class ActionTypes(Enum):
    writing = "writing"
    audio_recording = "audio_recording"
    audio_sending = "audio_sending"
    circle_recording = "circle_recording"
    circle_sending = "circle_sending"
    files_sending = "files_sending"


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
    chat_user_action = "chat_user_action"
    chat_changed = "chat_changed"


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
    content: str | None
    voice: SavedFile | None
    circle: SavedFile | None
    attachments: list[SavedFile]
    reply_to_id: int | None
    mentioned: list[int]
    readed_by: list[int]
    reactions: list[Reaction]
    created_at: datetime | None


@strawberry.type
class ChatActionUser:
    name: str
    id: int


@strawberry.type
class ChatAction:
    action: ActionTypes
    action_users: list[ChatActionUser]


@strawberry.type
class Chat:
    id: int
    avatar: SavedFile | None
    title: str
    type: str
    members: list[int]
    is_archived: bool
    owner_id: int
    admins: list[int]
    actions: list[ChatAction] = strawberry.field(default_factory=list)


@strawberry.type
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email_confirmed: bool
    phone_confirmed: bool
    avatar: SavedFile | None
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
