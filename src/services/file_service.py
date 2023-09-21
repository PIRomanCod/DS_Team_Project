import pickle

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import FAISS


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
    context = pickle.dumps(vectorstore)

    return context



