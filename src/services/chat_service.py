import pickle
from fastapi import Depends, HTTPException, status
import requests
from sqlalchemy.orm import Session

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from src.conf import messages
from src.conf.config import settings
from src.database.db import get_db
from src.repository import users as repository_users
from src.repository.chathistory import get_history_by_chat, create_message
from src.repository.chats import get_chat_by_id
from src.database.models import User, ChatHistory, Chat, Role


class ChatService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def get_conversation_chain(self, chat_id: int, user: User):  # має отримати chat_data
        chat = await get_chat_by_id(chat_id, self.db, user)
        context = chat.chat_data
        if context is None:
            raise HTTPException(status_code=404, detail="Chat data not found")

        vectorstore = pickle.loads(context)

        history = await get_history_by_chat(chat_id)

        llm = ChatOpenAI(model='gpt-3.5-turbo')
        # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
        memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(),
            memory=memory,
            verbose=True,
        )
        return conversation_chain

    async def create_question_and_response_in_history(self, chat_id: int, user_question: str, user: User):
        conversation_chain = await self.get_conversation_chain(chat_id)
        response = conversation_chain(user_question)
        body = {"message": user_question}
        await create_message(chat_id, body, self.db, user)

        return response


chat_service = ChatService()
