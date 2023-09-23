import pickle

import langchain
import requests
import streamlit as st
from dotenv import load_dotenv

from pages.src.auth_services import SERVER_URL, FILE_NAME

langchain.verbose = False


def get_chat_list():
    """
    The get_chat_list function returns a list of all the chats that the user is currently in.
    The function makes a GET request to /api/chats, which returns an array of chat objects.
    Each chat object contains information about the chat, including its id and name.

    :return: A list of chats
    """
    api_url = SERVER_URL + "/api/chats"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []


def create_message(chat_id, message):
    """
    The create_message function takes in a chat_id and message, then creates a new message
    in the database. It returns the response from the server.

    :param chat_id: Identify the chat
    :param message: Pass the message to be sent
    :return: A dictionary with the following keys:
    """
    api_url = SERVER_URL + f"/api/history/{chat_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    data = {"message": message}
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        return "Error creating question"


def get_history(chat_id):
    """
    The get_history function takes a chat_id as an argument and returns the history of that chat.
    It does this by making a GET request to the /api/history/.

    :param chat_id: Get the history of a specific chat
    :return: A list of messages in the chat
    """
    api_url = SERVER_URL + f"/api/history/{chat_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        st.write("In previous episodes...: ")
        return [item["message"] for item in response.json()]
    else:
        st.write("Chat's history: ")
        return "It's empty"


# main funk  Streamlit
def main():

    """
    The main function is the entry point for the module.
    It creates a list of chats from which to select, and then displays
    the chat history and allows users to ask questions about their documents.

    :return: A list of chats
    """
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
            if chat["chat_data"]:
                st.write("Chat has context, you can continue")
            else:
                st.write("Reload document, chat lost context")
            st.write(f"Selected chat: {selected_chat_index}")
            exist_history = get_history(chat["id"])
            st.write(exist_history)

    if selected_chat_id is not None:

        # Enter text for a question
        user_question = st.text_input("Ask a question about your documents:")

        # Button to create a question and receive an answer
        if st.button("Send a question"):
            response = create_message(selected_chat_id, user_question)
            st.write(f"Your question: {user_question}")
            st.write(f"Bot's answer: {response['message']}")


if __name__ == "__main__":
    load_dotenv()
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
