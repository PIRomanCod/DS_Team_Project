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

data_directory = settings.data_folder
root_directory = settings.root_directory
full_path = os.path.join(root_directory, data_directory)
#st.write("This message for cheking where are you try to save", full_path)

load_dotenv()


def get_pdf_text(pdf_doc) -> str:
    """
    The get_pdf_text function takes a PDF document as input and returns the text of that document.
    It does this by using the PyPDF2 library to read in each page of the PDF, extract its text, and then concatenate all
    of those pages into one string.

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
    pdf_doc = st.file_uploader("Upload your PDFs here and click on 'Process'", type='pdf')
    if pdf_doc:
        store_name = pdf_doc.name[:-4]

        if st.button("Process"):
            with st.spinner("Processing"):
                api_url = SERVER_URL + '/api/chats/'
                raw_text = get_pdf_text(pdf_doc)
                file_url = save_text_to_file(raw_text, full_path + store_name + '.txt')

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
