import hashlib


import streamlit as st
import requests


SERVER_URL = "http://localhost:8000"


def login(username, password):
    # password = hashlib.sha256(password.encode('utf-8'))
    data = {"username": username, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/login", data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def signup(username, email, password):
    # password = hashlib.sha256(password.encode('utf-8'))
    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/signup", data=data)
    return response.json()


def get_user_info(token_):
    headers = {"Authorization": f"Bearer {token_}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def login_page():
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        token_ = login(username, password)
        if token_:
            st.success("Success.")
            return token_
        else:
            st.error("Wrong username or password.")
    return None


def profile_page(token_):
    st.title("My profile")
    user_info = get_user_info(token_)
    if user_info:
        st.write(f"Username: {user_info['username']}")
        st.write(f"Email: {user_info['email']}")
    else:
        st.error("Unable connect")


def signup_page():
    st.title("SignUp")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm password", type="password")
    if st.button("Login"):
        if password == password_confirm:
            res = signup(username, email, password)
            if res.get("id"):
                st.success(f"Success. Confirm {res['email']}")
            else:
                st.error(f"{res['detail']}")
        else:
            st.error("Password not match")


def chat_page(token_):
    st.title("My profile")
    user_info = get_user_info(token_)
    if user_info:
        st.write(f"Username: {user_info['username']}")
        st.write(f"Email: {user_info['email']}")
    else:
        st.error("Unable connect")


if __name__ == '__main__':
    token = None
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose activity", ["SignUp", "Login", "Chat"])

    if page == "Login":
        token = login_page()
        if token:
            profile_page(token)
    elif page == "SignUp":
        signup_page()
    elif page == "Chat":
        signup_page()

