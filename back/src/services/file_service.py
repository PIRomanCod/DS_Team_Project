# import pickle
import os
import os
import pathlib

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from src.conf.config import settings
from dotenv import load_dotenv
load_dotenv()

EMBEDDINGS = OpenAIEmbeddings()
root_directory = pathlib.Path(__file__).parent.parent.parent.parent
data_folder = settings.data_folder
V_DB = "V_DB"
FULL_PATH = os.path.join(root_directory, data_folder, V_DB)


from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
# from langchain.vectorstores import FAISS
#
# from langchain.document_loaders import (
#     CSVLoader,
#     EverNoteLoader,
#     PyMuPDFLoader,
#     TextLoader,
#     UnstructuredEmailLoader,
#     UnstructuredEPubLoader,
#     UnstructuredHTMLLoader,
#     UnstructuredMarkdownLoader,
#     UnstructuredODTLoader,
#     UnstructuredPowerPointLoader,
#     UnstructuredWordDocumentLoader,
# )
#
# from dotenv import load_dotenv
#
# load_dotenv()
#
# supported_files = ['pdf', 'csv', 'doc', 'docx', 'enex', 'eml', 'epub', 'html', 'md', 'odt', 'ppt', 'pptx', 'txt']
#
# LOADER_MAPPING = {
#     ".csv": (CSVLoader, {}),
#     ".doc": (UnstructuredWordDocumentLoader, {}),
#     ".docx": (UnstructuredWordDocumentLoader, {}),
#     ".enex": (EverNoteLoader, {}),
#     ".eml": (UnstructuredEmailLoader, {}),
#     ".epub": (UnstructuredEPubLoader, {}),
#     ".html": (UnstructuredHTMLLoader, {}),
#     ".md": (UnstructuredMarkdownLoader, {}),
#     ".odt": (UnstructuredODTLoader, {}),
#     ".pdf": (PyMuPDFLoader, {}),
#     ".ppt": (UnstructuredPowerPointLoader, {}),
#     ".pptx": (UnstructuredPowerPointLoader, {}),
#     ".txt": (TextLoader, {"encoding": "utf8"}),
# }
#
#
#
# async def before_chat_insert(file_content):
#     with open(file_content, "r", encoding="utf-8") as file:
#         text = file.read()
#     text_splitter = CharacterTextSplitter(
#         separators=['\n\n', '\n', '(?=>\. )', ' ', ''],
#         # separator="\n",
#         chunk_size=1024,
#         chunk_overlap=64,
#         length_function=len
#     )
#     # chunks = text_splitter.split_text(text)
#     chunks = text_splitter.split_documents(text)
#
#     # embeddings = OpenAIEmbeddings()
#     # # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     #
#     # vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
#     # # vectorstore = Bagel.from_texts(cluster_name="testing", texts=text_chunks, embedding=embeddings)
#     # context = pickle.dumps(vectorstore)
#
#     return chunks
#     # return context

async def delete_source_file(path):
    file_path = path
    os.remove(file_path)


async def save_vectorstore(vectorstore, chat_id):
    vectorstore.save_local(FULL_PATH, index_name=str(chat_id))


async def load_vectorstore(chat_id):
    vectorstore = FAISS.load_local(FULL_PATH, index_name=str(chat_id),
                            embeddings=EMBEDDINGS)
    return vectorstore


def delete_vectorstore(chat_id):
    vectorstore_file_path_faiss = os.path.join(FULL_PATH, f"{chat_id}.faiss")
    vectorstore_file_path_pkl = os.path.join(FULL_PATH, f"{chat_id}.pkl")
    if os.path.exists(vectorstore_file_path_faiss):
        os.remove(vectorstore_file_path_faiss)
        os.remove(vectorstore_file_path_pkl)


async def merge_faiss_by_chat_ids(chat_ids):
    # Створюємо порожній об'єкт FAISS для злиття
    merged_faiss = FAISS()

    for chat_id in chat_ids:
        # Формуємо шлях до файлу FAISS для поточного чату
        vectorstore_file_path = os.path.join(FULL_PATH, f"{chat_id}.faiss")

        # Завантажуємо FAISS об'єкт з вказаного файлу
        faiss_obj = FAISS.load_local(vectorstore_file_path)

        # Злиття поточного об'єкта FAISS з іншим
        merged_faiss.merge_from(faiss_obj)

    return merged_faiss

