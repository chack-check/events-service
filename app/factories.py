from datetime import datetime

import msgspec

from app.gql.types import (
    ActionTypes,
    Chat,
    ChatAction,
    ChatActionUser,
    ChatEvent,
    ChatEventTypesEnum,
    Message,
    MessageEvent,
    MessageEventTypesEnum,
    MessageTypesEnum,
    Reaction,
    SavedFile,
    User,
    UserEvent,
    UserEventTypesEnum,
)
from app.schemas import (
    ChatActionData,
    ChatData,
    MessageData,
    ReactionData,
    SavedFileData,
    SystemEvent,
    UserEventData,
)


class SavedFileFactory:
    @classmethod
    def saved_file_from_system_event_data(cls, data: SavedFileData) -> SavedFile:
        return SavedFile(
            original_url=data["original_url"],
            original_filename=data["original_filename"],
            converted_url=data["converted_url"],
            converted_filename=data["converted_filename"],
        )


class UserEventFactory:
    @classmethod
    def user_from_system_event_data(cls, data: UserEventData) -> User:
        return User(
            id=data["id"],
            username=data["username"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            email_confirmed=data["email_confirmed"],
            phone_confirmed=data["phone_confirmed"],
            last_seen=datetime.fromisoformat(data["last_seen"]) if data["last_seen"] else None,
            status=data["status"],
            middle_name=data["middle_name"],
            phone=data["phone"],
            email=data["email"],
            avatar=SavedFileFactory.saved_file_from_system_event_data(data["avatar"]) if data["avatar"] else None,
        )

    @classmethod
    def user_event_from_system_event(cls, event: SystemEvent) -> UserEvent:
        system_event_data = msgspec.json.decode(event.data)
        return UserEvent(
            included_users=event.included_users,
            event_type=UserEventTypesEnum(event.event_type),
            user=cls.user_from_system_event_data(system_event_data),
        )


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
        attachments = (
            [
                SavedFileFactory.saved_file_from_system_event_data(attachment)
                for attachment in system_event_data["attachments"]
            ]
            if system_event_data["attachments"]
            else []
        )
        return Message(
            id=system_event_data["id"],
            chat_id=system_event_data["chatId"],
            sender_id=system_event_data["senderId"],
            type=MessageTypesEnum(system_event_data["type"]),
            content=system_event_data["content"],
            voice=(
                SavedFileFactory.saved_file_from_system_event_data(system_event_data["voice"])
                if system_event_data["voice"]
                else None
            ),
            circle=(
                SavedFileFactory.saved_file_from_system_event_data(system_event_data["circle"])
                if system_event_data["circle"]
                else None
            ),
            attachments=attachments,
            reply_to_id=system_event_data["replyToId"],
            mentioned=system_event_data["mentioned"] or [],
            readed_by=system_event_data["readedBy"] or [],
            reactions=(
                [cls.reaction_from_event_data(reaction) for reaction in system_event_data["reactions"]]
                if system_event_data["reactions"]
                else []
            ),
            created_at=(
                datetime.fromisoformat(system_event_data["createdAt"]) if system_event_data["createdAt"] else None
            ),
        )

    @classmethod
    def message_event_from_system_event(cls, event: SystemEvent) -> MessageEvent:
        system_event_data = msgspec.json.decode(event.data)
        return MessageEvent(
            included_users=event.included_users,
            event_type=MessageEventTypesEnum(event.event_type),
            message=cls.message_from_system_event_data(system_event_data),
        )


class ChatActionsFactory:
    @classmethod
    def chat_actions_from_system_event_data(cls, data: list[ChatActionData]) -> list[ChatAction]:
        chat_actions = []
        for action in data:
            chat_action_users = []
            for user in action["action_users"]:
                chat_action_users.append(ChatActionUser(name=user["name"], id=user["id"]))

            chat_actions.append(ChatAction(action=ActionTypes(action["action"]), action_users=chat_action_users))

        return chat_actions


class ChatEventFactory:
    @classmethod
    def chat_from_system_event_data(cls, system_event_data: ChatData) -> Chat:
        return Chat(
            id=system_event_data["id"],
            avatar=(
                SavedFileFactory.saved_file_from_system_event_data(system_event_data["avatar"])
                if system_event_data["avatar"]
                else None
            ),
            title=system_event_data["title"],
            type=system_event_data["type"],
            members=system_event_data["members"] or [],
            is_archived=system_event_data["isArchived"],
            owner_id=system_event_data["ownerId"],
            admins=system_event_data["admins"] or [],
            actions=(
                ChatActionsFactory.chat_actions_from_system_event_data(system_event_data["actions"])
                if system_event_data["actions"]
                else []
            ),
        )

    @classmethod
    def chat_event_from_system_event(cls, event: SystemEvent) -> ChatEvent:
        system_event_data = msgspec.json.decode(event.data)
        return ChatEvent(
            event_type=ChatEventTypesEnum(event.event_type),
            included_users=event.included_users,
            chat=cls.chat_from_system_event_data(system_event_data),
        )
