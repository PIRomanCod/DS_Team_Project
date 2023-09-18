from fastapi import APIRouter, HTTPException, Depends, status, Request, Query
from sqlalchemy.orm import Session
from typing import List

from src.database.db import get_db
from src.schemas import ChatHistoryBase, ChatHistoryModel
from src.repository import chathistory as repository_history
from src.repository import chats as repository_chats
from src.services.auth import auth_service
from src.conf import messages
from src.services.role import RoleAccess
from src.database.models import User, Role, Chat

router = APIRouter(prefix='/history', tags=["history"])

allowed_get_history = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_add_messages = RoleAccess([Role.user, Role.admin])
# allowed_edit_chats = RoleAccess([Role.admin, Role.moderator, Role.user])
# allowed_delete_chats = RoleAccess([Role.admin, Role.moderator, Role.user])


@router.post("/{chat_id}", response_model=ChatHistoryModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_add_messages)])
async def create_message(chat_id: int, body: ChatHistoryBase, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    The **create_chat** function creates a new chat for the user with the given id.

    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the current user
    :return: A chat object, which is then serialized as json
    """
    new_message = await repository_history.create_message(chat_id, body, db, current_user)
    return new_message

#
# @router.get("/", response_model=List[ChatModel], status_code=status.HTTP_200_OK,
#             dependencies=[Depends(allowed_get_chats)])
# async def get_chats(limit: int = Query(10, le=50), offset: int = 0,
#                      current_user: User = Depends(auth_service.get_current_user),
#                      db: Session = Depends(get_db)):
#     """
#     The **get_chats** function gets all the chats from the database.
#
#     :param limit: int: The number of images to return
#     :param offset: int: The number of images to skip
#     :param current_user: User: The user object
#     :param db: Session: A connection to our Postgres SQL database.
#     :return: A list of chat objects
#     """
#     chats = await repository_chats.get_chats(limit, offset, current_user, db)
#     if chats is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)
#     return chats


@router.get("/{chat_id}", response_model=List[ChatHistoryModel], dependencies=[Depends(allowed_get_history)])
async def get_history(chat_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    """
    The **get_chat** function returns a specified chat from the database.

    :param chat_id: int: Pass the chat id to the function
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user from the database
    :return: The chat object
    """
    history = await repository_history.get_history_by_chat(chat_id, db)
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.CHAT_NOT_FOUND)
    return history

#
# @router.put("/{chat_id}", response_model=ChatUpdate, dependencies=[Depends(allowed_edit_chats)])
# async def update_chat(chat_id: int, body: ChatBase, db: Session = Depends(get_db),
#                       current_user: User = Depends(auth_service.get_current_user)):
#     """
#     The **update_chat** function allows a user to edit their own chat.
#
#     :param chat_id: int: Identify the chat to be edited
#     :param body: ChatBase: Pass the chat body to the update_chat function
#     :param db: Session: Get the database session
#     :param current_user: User: Get the user who is currently logged-in
#     :return: None, but the function expects a ChatBase object
#     """
#     updated_chat = await repository_chats.update_chat(chat_id, body, db, current_user)
#     if updated_chat is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.CHAT_NOT_FOUND)
#     return updated_chat

#
# @router.delete("/{chat_id}", response_model=ChatModel,
#                dependencies=[Depends(allowed_delete_chats)])
# async def delete_chat(chat_id: int, db: Session = Depends(get_db),
#                       current_user: User = Depends(auth_service.get_current_user)):
#     """
#     The **delete_chat** function deletes a specified chat from the database.
#
#     :param chat_id: int: Specify the chat that is to be deleted
#     :param db: Session: Get the database session from the dependency
#     :param current_user: User: Check if the user is logged-in
#     :return: The deleted chat
#     """
#     deleted_chat = await repository_chats.delete_chat(chat_id, db, current_user)
#     if deleted_chat is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.CHAT_NOT_FOUND)
#     return deleted_chat