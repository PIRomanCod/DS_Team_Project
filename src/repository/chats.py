from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from src.database.models import User, Chat, Role
from src.schemas import ChatBase

import requests

from src.services.file_service import before_chat_insert


async def create_chat(body: ChatBase, db: Session, user: User) -> Chat:
    """
    The **create_chat** function adds a new chat to the database.

    :param db: Session: Access the database
    :param user: User: Get the user_id from the logged-in user
    :return: A chat object
    """
    # response = body.file_url
    llm_state = await before_chat_insert(body.file_url)

    new_chat = Chat(title_chat=body.title_chat, chat_data=llm_state, file_url=body.file_url, user_id=user.id)
    # else:
    # new_chat = Chat(title_chat=body.title_chat, file_url=body.file_url, user_id=user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


async def update_chat(chat_id: int, body: ChatBase, db: Session, user: User) -> Chat | None:
    """
    The **update_chat** function allows a user to edit their own chat.

    :param chat_id: int: Find the chat in the database
    :param body: ChatBase: Pass the data from the request body to this function
    :param db: Session: Connect to the database
    :param user: User: Check if the user is an admin, moderator or the author of the chat
    :return: A chat object
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        if user.roles in [Role.admin, Role.moderator] or chat.user_id == user.id:
            chat.title_chat = body.title_chat
            chat.updated_at = func.now()
            db.commit()
    return chat


async def delete_chat(chat_id: int, db: Session, user: User) -> None:
    """
    The **delete_chat** function deletes a chat from the database. The chat can be deleted by Admin and Moderator #my own chat????

    :param chat_id: int: Identify the chat to be deleted
    :param db: Session: Connect to the database
    :param user: User: Check if the user is Admin or Moderator and authorized to delete a chat
    :return: The chat that was deleted
    """
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if chat:
        if user.roles in [Role.admin, Role.moderator] or chat.user_id == user.id:
            db.delete(chat)
            db.commit()
    return chat


async def get_chat_by_id(chat_id: int, db: Session, user: User) -> Chat | None:
    """
    The **get_chat_by_id** function returns a chat from the database by chat_id.

    :param chat_id: int: Specify the id of the chat that we want to retrieve
    :param db: Session: Access the database
    :param user: User: Check if the user is authorized to see chat
    :return: The chat with the given id, if it exists
    """
    return db.query(Chat).filter(and_(Chat.id == chat_id, Chat.user_id == user.id)).first()


async def get_chats(limit: int, offset: int, user: User, db: Session):
    """
    The **get_chats** function gets all the chats from the database.

    :param limit: int: The number of images to return
    :param offset: int: The number of images to skip
    :param user: User: The user object
    :param db: Session: A connection to our Postgres SQL database.
    :return: A list of chats objects
    """
    chats = db.query(Chat).filter(and_(Chat.user_id == user.id)). \
        order_by(desc(Chat.created_at)).limit(limit).offset(offset).all()
    return chats
