import pickle

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader

import requests
import os

from htmlTemplates import css, bot_template, user_template


from pages.src.auth_services import SERVER_URL, FILE_NAME

from src.conf.config import settings
import json

data_directory = settings.data_folder
root_directory = settings.root_directory
full_path = os.path.join(root_directory, data_directory)
st.write("This message for cheking where are you try to save", full_path)

load_dotenv()

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def save_text_to_file(text, path):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    return path

def main():
    # load_dotenv()
    # st.set_page_config(page_title="Your own AI chat",
    #                    page_icon="👋")

    st.write(css, unsafe_allow_html=True)

    st.subheader("Your documents")
    pdf_doc = st.file_uploader("Upload your PDFs here and click on 'Process'", type='pdf')
    # st.write(pdf_doc)
    if pdf_doc:
        store_name = pdf_doc.name[:-4]
        # st.write(f'{store_name}')

        if st.button("Process"):
            with st.spinner("Processing"):
                api_url = SERVER_URL+'/api/chats/'
                # get pdf text and save to .txt
                raw_text = get_pdf_text(pdf_doc)
                file_url = save_text_to_file(raw_text, full_path + store_name + '.txt')

                data = {
                    "title_chat": f"{store_name}",
                    "file_url": f"{file_url}"
                }
                # st.write(data)
                data_json = json.dumps(data)
                # st.write(data_json)
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    'Content-Type': 'application/json'
                }
                # st.write(headers)

                response = requests.post(api_url, data=data_json, headers=headers)

                if response.status_code == 201:
                    st.success("Chat created successfully.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")


if __name__ == '__main__':
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()

