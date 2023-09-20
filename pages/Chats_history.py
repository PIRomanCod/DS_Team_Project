import streamlit as st
import requests
import json
import pickle
from dotenv import load_dotenv
import langchain

from pages.Auth import SERVER_URL, FILE_NAME
from src.conf.config import settings
from htmlTemplates import css, bot_template, user_template


langchain.verbose = False


# function for receiving a list of chats from the server
def get_chat_list():
    api_url = SERVER_URL + "/api/chats"
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# function for creating a question for the chat
def create_message(chat_id, message):
    api_url = SERVER_URL + f"/api/history/{chat_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    data = {"message": message}
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 201:
        return response.json()#["response"]
    else:
        return "Error creating question"

# main funk  Streamlit
def main():
    st.set_page_config(page_title="Your own AI chat",
                       page_icon=":sunglasses:")

    st.write(css, unsafe_allow_html=True)

    st.title("Exist chats")

    # get list of chats from the server
    chat_list = get_chat_list()

    # display a list of chats for selection
    selected_chat_index = st.selectbox("Select a chat:", [chat["title_chat"] for chat in chat_list])

    # find the chat_id of the selected chat
    selected_chat_id = None
    for chat in chat_list:
        if chat["title_chat"] == selected_chat_index:
            selected_chat_id = chat["id"]

    if selected_chat_id is not None:
        st.write(f"Selected chat: {selected_chat_index}")

        # Enter text for a question
        user_question = st.text_input("Ask a question about your documents:")

        # Button to create a question and receive an answer
        if st.button("Send a question"):
            response = create_message(selected_chat_id, user_question)
            st.write(f"Bot's answer: {response}")

if __name__ == "__main__":
    load_dotenv()
    with open(FILE_NAME, "rb") as fh:
        token = pickle.load(fh)
    main()