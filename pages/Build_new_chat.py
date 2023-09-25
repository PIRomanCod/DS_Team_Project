import json
import os
import pickle

import requests
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from htmlTemplates import css
from pages.src.auth_services import SERVER_URL, FILE_NAME
from src.conf.config import settings

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)


data_directory = settings.data_folder
root_directory = settings.root_directory
full_path = os.path.join(root_directory, data_directory)

load_dotenv()

supported_files = ['pdf', 'csv', 'docx', 'eml', 'epub', 'html', 'md', 'pptx', 'txt']

LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".eml": (UnstructuredEmailLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}


def get_text(pdf_doc) -> str:
    """
    The get_text function takes a document as input and returns the text of that document.
    It does this by using the langchain.document_loaders  to read in each page of the supported_files,
    extract its text, and then concatenate all of those pages into one string.

    :param pdf_doc: Specify the file path of the pdf document that you want to extract text from
    :return: A string of text from the pdf document
    """
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def save_text_to_file(text, path):
    """
    The save_text_to_file function takes a string and saves it to a file.

    :param text: Pass the text to be written to a file
    :param path: Specify the location where the file should be saved
    :return: The path of the file that was written to
    """
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    return path


def main():
    """
    The main function is the entry point of the module.
    It creates a bar with two options: upload and process PDF.

    :return: The main function
    """
    st.write(css, unsafe_allow_html=True)

    st.subheader("Your documents")
    pdf_doc = st.file_uploader("Upload your PDFs here and click on 'Process'", type=supported_files)
    if pdf_doc:
        store_name, ext = pdf_doc.name.split(".")
        if ext not in supported_files:
            st.warning(f"Unsupported file extension '{ext}'")

        if st.button("Process"):
            with st.spinner("Processing"):
                api_url = SERVER_URL + '/api/chats/'
                temp_file_path = os.path.join(full_path, pdf_doc.name)
                with open(temp_file_path, "wb") as temp_file:
                    temp_file.write(pdf_doc.read())

                if ext == 'txt':
                    text_to_save = None
                else:
                    loader_class, loader_args = LOADER_MAPPING['.' + ext]
                    loader = loader_class(temp_file_path, **loader_args)
                    loader.load()
                    raw_text = loader.load()
                    if isinstance(raw_text, list):
                        text_to_save = raw_text[0].page_content
                    else:
                        text_to_save = raw_text.page_content

                if text_to_save is not None:
                    file_url = save_text_to_file(text_to_save, full_path + store_name + '.txt')
                    os.remove(temp_file_path)
                else:
                    file_url = temp_file_path


                data = {
                    "title_chat": f"{store_name}",
                    "file_url": f"{file_url}"
                }
                data_json = json.dumps(data)

                headers = {
                    "Authorization": f"Bearer {access_token}",
                    'Content-Type': 'application/json'
                }

                response = requests.post(api_url, data=data_json, headers=headers)

                if response.status_code == 201:
                    st.success("Chat created successfully.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
