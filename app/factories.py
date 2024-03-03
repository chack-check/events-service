import msgspec

from app.gql.types import (
    Chat,
    ChatEvent,
    ChatEventTypesEnum,
    Message,
    MessageEvent,
    MessageEventTypesEnum,
    MessageTypesEnum,
    Reaction,
)
from app.schemas import ChatData, MessageData, ReactionData, SystemEvent


class MessageEventFactory:
    @classmethod
    def reaction_from_event_data(cls, reaction: ReactionData) -> Reaction:
        return Reaction(
            id=reaction["id"],
            user_id=reaction["user_id"],
            content=reaction["content"],
        )

    @classmethod
    def message_from_system_event_data(cls, system_event_data: MessageData) -> Message:
        return Message(
            id=system_event_data["id"],
            chat_id=system_event_data["chat_id"],
            sender_id=system_event_data["sender_id"],
            type=MessageTypesEnum(system_event_data["type"]),
            content=system_event_data["content"],
            voice_url=system_event_data["voice_url"],
            circle_url=system_event_data["circle_url"],
            attachments=system_event_data["attachments"],
            reply_to_id=system_event_data["reply_to_id"],
            mentioned=system_event_data["mentioned"] or [],
            readed_by=system_event_data["readed_by"] or [],
            reactions=[cls.reaction_from_event_data(reaction) for reaction in system_event_data["reactions"]] if system_event_data["reactions"] else [],
            datetime=system_event_data["CreatedAt"],
        )

    @classmethod
    def message_event_from_system_event(cls, event: SystemEvent) -> MessageEvent:
        system_event_data = msgspec.json.decode(event.data)
        return MessageEvent(
            included_users=event.included_users,
            event_type=MessageEventTypesEnum(event.event_type),
            message=cls.message_from_system_event_data(system_event_data),
        )


class ChatEventFactory:
    @classmethod
    def chat_from_system_event_data(cls, system_event_data: ChatData) -> Chat:
        return Chat(
            id=system_event_data["id"],
            avatar_url=system_event_data["avatar_url"],
            title=system_event_data["title"],
            type=system_event_data["type"],
            members=system_event_data["members"] or [],
            is_archived=system_event_data["is_archived"],
            owner_id=system_event_data["owner_id"],
            admins=system_event_data["admins"] or [],
        )

    @classmethod
    def chat_event_from_system_event(cls, event: SystemEvent) -> ChatEvent:
        system_event_data = msgspec.json.decode(event.data)
        return ChatEvent(
            event_type=ChatEventTypesEnum(event.event_type),
            included_users=event.included_users,
            chat=cls.chat_from_system_event_data(system_event_data),
        )
