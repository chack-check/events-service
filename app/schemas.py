from typing import TypedDict

from pydantic import BaseModel


class UserData(BaseModel):
    id: int


class SystemEvent(BaseModel):
    event_type: str
    included_users: list[int]
    data: str


class SavedFileData(TypedDict):
    original_url: str
    original_filename: str
    converted_url: str | None
    converted_filename: str | None


class UserEventData(TypedDict):
    id: int
    username: str
    first_name: str
    last_name: str
    email_confirmed: bool
    phone_confirmed: bool
    avatar: SavedFileData
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
    chat_id: int
    sender_id: int
    type: str
    content: str
    voice: SavedFileData
    circle: SavedFileData
    attachments: list[SavedFileData]
    reply_to_id: int
    mentioned: list[int]
    readed_by: list[int]
    CreatedAt: str
    reactions: list[ReactionData]


class ChatActionUserData(TypedDict):
    name: str
    id: int


class ChatActionData(TypedDict):
    action: str
    action_users: list[ChatActionUserData]


class ChatData(TypedDict):
    id: int
    avatar: SavedFileData
    title: str
    type: str
    members: list[int]
    is_archived: bool
    owner_id: int
    admins: list[int]
    actions: list[ChatActionData]
    CreatedAt: str
