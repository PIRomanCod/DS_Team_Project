import pickle

import langchain
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import requests
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.vectorstores import Bagel
from langchain.callbacks import get_openai_callback
import cloudinary
import cloudinary.uploader
from src.conf.config import settings
import json
import requests
from io import BytesIO
import os

load_dotenv()
langchain.verbose = False


async def before_chat_insert(file_content):


    with open(file_content, "r", encoding="utf-8") as file:
        text = file.read()
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    # vectorstore = Bagel.from_texts(cluster_name="testing", texts=text_chunks, embedding=embeddings)


    llm = ChatOpenAI(model='gpt-3.5-turbo')
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    llm_state = pickle.dumps(conversation_chain)

    return llm_state



