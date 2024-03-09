from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel


class UserData(BaseModel):
    id: int


class SystemEvent(BaseModel):
    event_type: str
    included_users: list[int]
    data: str


class UserAvatarData(TypedDict):
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
    avatar: UserAvatarData
    last_seen: datetime | None
    status: str | None
    middle_name: str | None
    phone: str | None
    email: str | None


class ReactionData(TypedDict):
    id: int
    user_id: int
    content: str
    CreatedAt: datetime


class MessageData(TypedDict):
    id: int
    chat_id: int
    sender_id: int
    type: str
    content: str
    voice_url: str
    circle_url: str
    attachments: list[str]
    reply_to_id: int
    mentioned: list[int]
    readed_by: list[int]
    CreatedAt: datetime
    reactions: list[ReactionData]


class ChatData(TypedDict):
    id: int
    avatar_url: str
    title: str
    type: str
    members: list[int]
    is_archived: bool
    owner_id: int
    admins: list[int]
    CreatedAt: datetime
