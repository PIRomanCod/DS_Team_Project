from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from src.database.models import User, ChatHistory, Chat, Role
from src.schemas import ChatHistoryBase


async def create_message(chat_id: int, body: ChatHistoryBase, db: Session, user: User) -> ChatHistory:
    """
    The **create_message** function adds a new history to the database.

    :param db: Session: Access the database
    :param user: User: Get the user_id from the logged-in user
    :param chat: Chat: Get the chat_id
    :return: A new chat_history object
    """
    new_chat_history = ChatHistory(message=body.message, user_id=user.id, chat_id=chat_id)
    db.add(new_chat_history)
    db.commit()
    db.refresh(new_chat_history)
    return new_chat_history


# async def update_chat(chat_id: int, body: ChatBase, db: Session, user: User) -> Chat | None:
#     """
#     The **update_chat** function allows a user to edit their own chat.
#
#     :param chat_id: int: Find the chat in the database
#     :param body: ChatBase: Pass the data from the request body to this function
#     :param db: Session: Connect to the database
#     :param user: User: Check if the user is an admin, moderator or the author of the chat
#     :return: A chat object
#     """
#     chat = db.query(Chat).filter(Chat.id == chat_id).first()
#     if chat:
#         if user.roles in [Role.admin, Role.moderator] or chat.user_id == user.id:
#             chat.chat = body.chat
#             chat.updated_at = func.now()
#             db.commit()
#     return chat


# async def delete_chat(chat_id: int, db: Session, user: User) -> None:
#     """
#     The **delete_chat** function deletes a chat from the database. The chat can be deleted by Admin and Moderator #my own chat????
#
#     :param chat_id: int: Identify the chat to be deleted
#     :param db: Session: Connect to the database
#     :param user: User: Check if the user is Admin or Moderator and authorized to delete a chat
#     :return: The chat that was deleted
#     """
#     chat = db.query(Chat).filter(Chat.id == chat_id).first()
#     if chat:
#         if user.roles in [Role.admin, Role.moderator] or chat.user_id == user.id:
#             db.delete(chat)
#             db.commit()
#     return chat


async def get_history_by_chat(chat_id: int, db: Session):
    """
    The **get_history_by_chat** function returns a history from the database by chat_id and user.

    :param chat_id: int: Specify the id of the chat that we want to retrieve
    :param db: Session: Access the database
    # :param user: User: Check if the user is authorized to see chat
    :return: The messages with the given id, if it exists
    """
    return db.query(ChatHistory).filter(and_(ChatHistory.chat_id == chat_id)). \
        order_by(ChatHistory.created_at).all()
