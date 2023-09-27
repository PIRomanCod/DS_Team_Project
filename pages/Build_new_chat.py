import os
import pickle
from PyPDF2 import PdfReader

import streamlit as st
from dotenv import load_dotenv
from langchain.document_loaders import (
    CSVLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from htmlTemplates import css
from pages.src.auth_services import FILE_NAME
from pages.src.build_new_chat_services import save_text_to_file, search_duplicate, set_data_url, get_pdf_text
from pages.src.build_new_chat_services import full_path

load_dotenv()

supported_files = ['pdf', 'csv', 'docx', 'eml', 'epub', 'html', 'md', 'pptx', 'txt']

LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".eml": (UnstructuredEmailLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".pdf": (PdfReader),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}


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
                if not search_duplicate(store_name):

                    temp_file_path = os.path.join(full_path, pdf_doc.name)

                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(pdf_doc.read())

                    if ext == 'txt':
                        text_to_save = None
                    if ext == 'pdf':
                        text_to_save = get_pdf_text(temp_file_path)
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
                        file_url = save_text_to_file(text_to_save, os.path.join(full_path, store_name + '.txt'))
                        os.remove(temp_file_path)
                    else:
                        file_url = temp_file_path

                    response = set_data_url(store_name, file_url, access_token)

                    if response.status_code == 201:
                        st.success("Chat created successfully.")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")

                else:
                    st.error("Filename conflict. Change filename and try again")


if __name__ == '__main__':
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
