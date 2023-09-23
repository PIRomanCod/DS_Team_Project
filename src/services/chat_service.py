import pickle
from fastapi import Depends, HTTPException, status
import requests
import asyncio

from sqlalchemy.orm import Session

from langchain import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

from src.conf import messages
# from src.conf.config import settings
# from src.database.db import get_db
# from src.repository import users as repository_users
# from src.repository.chathistory import get_history_by_chat, create_message
from src.repository.chats import get_chat_by_id
from src.database.models import User, ChatHistory, Chat, Role
import asyncio


async def get_context(chat_id: int, db: Session, user: User):  # має отримати chat_data
    chat = await get_chat_by_id(chat_id, db, user)
    context = chat.file_url
    if context is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=messages.NOT_FOUND)

    with open(context, "r", encoding="utf-8") as file:
        text = file.read()

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)



    # vectorstore = pickle.loads(context)
    return chunks #context

def get_conversation_chain(user_question, context):

    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    #
    vectorstore = FAISS.from_texts(texts=context, embedding=embeddings)
    # vectorstore = Bagel.from_texts(cluster_name="testing", texts=text_chunks, embedding=embeddings)


    llm = ChatOpenAI(model='gpt-3.5-turbo')
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        # chain_type='stuff',
        retriever=vectorstore.as_retriever(),
        memory=memory,
        # verbose=True,
    )

    # response = conversation_chain({'question': user_question})
    # return conversation_chain

# def handle_userinput(user_question, context):
#     conversation = get_conversation_chain(context)
    response = conversation_chain({'question': user_question})
    chat_history = response['chat_history']

# for extract  question/answer chain
    response_dict = {'user_messages': [], 'bot_messages': []}

    for i, message in enumerate(chat_history):
        if i % 2 == 0:
            response_dict['user_messages'].append(message.content)
        else:
            response_dict['bot_messages'].append(message.content)

    return str(response_dict)

