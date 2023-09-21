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

router = APIRouter(prefix='/start', tags=["chat_service"])


@router.post("/{chat_id}", response_model=str)
async def ask_question():
    pass