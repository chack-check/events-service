from typing import TypedDict

from pydantic import BaseModel


class UserData(BaseModel):
    id: int


class SystemEvent(BaseModel):
    event_type: str
    included_users: list[int]
    data: str


class SavedFileData(TypedDict):
    originalUrl: str
    originalFilename: str
    convertedUrl: str | None
    convertedFilename: str | None


class UserEventData(TypedDict):
    id: int
    username: str
    first_name: str
    last_name: str
    email_confirmed: bool
    phone_confirmed: bool
    avatar: SavedFileData | None
    last_seen: str | None
    status: str | None
    middle_name: str | None
    phone: str | None
    email: str | None


class ReactionData(TypedDict):
    id: int
    user_id: int
    content: str
    CreatedAt: str


class MessageData(TypedDict):
    id: int
    chatId: int
    senderId: int
    type: str
    content: str | None
    voice: SavedFileData | None
    circle: SavedFileData | None
    attachments: list[SavedFileData]
    replyToId: int | None
    mentioned: list[int]
    readedBy: list[int]
    createdAt: str | None
    reactions: list[ReactionData]


class ChatActionUserData(TypedDict):
    name: str
    id: int


class ChatActionData(TypedDict):
    action: str
    action_users: list[ChatActionUserData]


class ChatData(TypedDict):
    id: int
    avatar: SavedFileData | None
    title: str
    type: str
    members: list[int]
    isArchived: bool
    ownerId: int
    admins: list[int]
    actions: list[ChatActionData]
