import pickle

import langchain
import streamlit as st
from dotenv import load_dotenv

from pages.src.auth_services import FILE_NAME
from pages.src.chats_history_services import get_chat_list, create_message, get_history

langchain.verbose = False

def delete_chat(chat_id):
    """
    The delete_chat function takes in a chat_id and deletes the chat from the database.
        It returns an error message if the chat is not found, or a success message if it is.

    :param chat_id: Specify which chat to delete
    :return: A response object
    """
    api_url = SERVER_URL + f"/api/chats/{chat_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 404:
        st.warning("Chat not found.")
    else:
        st.error("Chat deleted successfully.")

        
def get_chat_history(chat_id):
    res = get_history(chat_id, access_token)
    if res.status_code == 200:
        st.write("In previous episodes...: ")
        return [item["message"] for item in res.json()]
    else:
        st.write("Chat's history: ")
        return "It's empty"


# main funk  Streamlit
def main():
    """
    The main function is the entry point for the application.
    It creates a Streamlit app and runs it.

    :return: The access token
    :doc-author: Trelent
    """
    st.title("Exist chats")

    # get list of chats from the server
    chat_list = get_chat_list(access_token)

    # display a list of chats for selection
    selected_chat_index = st.selectbox("Select a chat:", [chat["title_chat"] for chat in chat_list])

    # find the chat_id of the selected chat
    selected_chat_id = None
    for chat in chat_list:
        if chat["title_chat"] == selected_chat_index:
            selected_chat_id = chat["id"]

            if st.button("Delete Chat"):
                if selected_chat_id:
                    delete_chat(selected_chat_id)

            if chat["chat_data"]:
                st.write("Chat has context, you can continue")
            else:
                st.write("Reload document, chat lost context")
            st.write(f"Selected chat: {selected_chat_index}")
            exist_history = get_chat_history(chat["id"])
            st.write(exist_history)

    if selected_chat_id is not None:

        # Enter text for a question
        user_question = st.text_input("Ask a question about your documents:")

        # Button to create a question and receive an answer
        if st.button("Send a question"):
            response = create_message(selected_chat_id, user_question, access_token)
            st.write(f"Your question: {user_question}")
            st.write(f"Bot's answer: {response['message']}")


if __name__ == "__main__":
    load_dotenv()
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
