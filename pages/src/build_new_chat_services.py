import os
import json

import requests
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from src.conf.config import settings
from pages.src.auth_services import SERVER_URL, FILE_NAME

data_directory = settings.data_folder
root_directory = os.getcwd()
full_path = os.path.join(root_directory, data_directory)


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


def search_duplicate(store_name):
    """
    The search_duplicate function takes in a store name as an argument and searches the directory for a file with that
    store name. If it finds one, it returns True. Otherwise, it returns None.

    :param store_name: Search for a file with the same name as the store
    :return: True if the file exists, none otherwise
    :doc-author: Trelent
    """
    search_txt = f"{store_name}.txt"
    if os.path.exists(full_path) and os.path.isdir(full_path):
        file_list = os.listdir(full_path)
        if search_txt in file_list:
            return True
    return None


def set_data_url(store_name, file_url, acc_token):
    """
    The set_data_url function takes in the store name, file url, and access token as parameters.
    It then creates a dictionary with the title_chat key set to the store name and file_url key set to
    the file url. It then converts this dictionary into JSON format using json.dumps(). The function
    then sets up headers for authorization and content type (JSON). Finally it returns a POST request
    to our API server with data being equal to our JSON formatted data.

    :param store_name: Set the title of the chat
    :param file_url: Send the url of the file to be uploaded
    :param acc_token: Authenticate the user
    :return: A response object
    :doc-author: Trelent
    """
    api_url = SERVER_URL + '/api/chats/'
    data = {
        "title_chat": f"{store_name}",
        "file_url": f"{file_url}"
    }
    data_json = json.dumps(data)

    headers = {
        "Authorization": f"Bearer {acc_token}",
        'Content-Type': 'application/json'
    }

    return requests.post(api_url, data=data_json, headers=headers)


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


load_dotenv()
