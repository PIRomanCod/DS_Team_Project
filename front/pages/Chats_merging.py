import pickle

# import langchain
import streamlit as st
from dotenv import load_dotenv

from pages.src.auth_services import FILE_NAME
from pages.src.chats_history_services import get_chat_list, merge_chats

# langchain.verbose = False

# main funk  Streamlit
def main():
    """
    The main function is the entry point for the application.
    It creates a Streamlit app and runs it.

    :return: The access token
    """
    st.title("Exist chats")

    # get list of chats from the server
    chat_list = get_chat_list(access_token)

    selected_chats_to_merge = st.multiselect("Select chats to merge:",
                                             [chat["title_chat"] for chat in chat_list])
    # Button to merge chats
    merge_button = st.button("Merge Chats")
    if merge_button:

        selected_chat_ids = [chat["id"] for chat in chat_list if chat["title_chat"] in selected_chats_to_merge]
        st.write(selected_chat_ids)
        if len(selected_chat_ids) >= 2:
            response = merge_chats(selected_chat_ids, access_token)
            st.write(f"Merge request sent. Server response: {response}")

    # Refresh chat list to reflect changes (this is an example, you can adjust it as needed)
    chat_list = get_chat_list(access_token)


if __name__ == "__main__":
    load_dotenv()
    with open(FILE_NAME, "rb") as fh:
        access_token, refresh_token = pickle.load(fh)

    main()
