import hashlib
import json
import pickle

import streamlit as st
import requests


st.set_page_config(
    page_title="Auth",
    page_icon="lock",
)

FILE_NAME = 'data.bin'

SERVER_URL = "http://localhost:8000"


def load_token(filename=FILE_NAME):
    try:
        with open(FILE_NAME, "rb") as fh:
            result = pickle.load(fh)
            return result
    except IOError:
        with open(FILE_NAME, "wb") as fh:
            pickle.dump((None, None), fh)


def save_token(acc_token, ref_token):
    with open(FILE_NAME, "wb") as fh:
        pickle.dump((acc_token, ref_token), fh)


def login(username, password):
    # password = hashlib.sha256(password.encode('utf-8'))
    data = {"username": username, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/login", data=data)
    if response.status_code == 200:
        return response.json()["access_token"], response.json()["refresh_token"]
    return None


def signup(username, email, password):
    # password = hashlib.sha256(password.encode('utf-8'))
    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/signup", data=json.dumps(data))
    return response.json()


def get_user_info(acc_token, ref_token):
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        return response.json()
    acc_token, ref_token = get_refresh_token(acc_token, ref_token)
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        save_token(acc_token, ref_token)
        return response.json()
    return None


def get_refresh_token(acc_token, ref_token):
    headers = {"Authorization": f"Bearer {ref_token}"}
    response = requests.get(f"{SERVER_URL}/api/auth/refresh_token", headers=headers)
    if response.json().get("access_token"):
        return response.json()["access_token"], response.json()["refresh_token"]
    return None, None


def login_page():
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        acc_token, ref_token = login(username, password)
        if acc_token:
            st.success("Success.")
            profile_page(acc_token, ref_token)
            return acc_token, ref_token
        else:
            acc_token, ref_token = get_refresh_token(ref_token)
            if not acc_token:
                st.error("Wrong username or password.")
    return None, None


def start_page():
    st.title("Login for use all features")


def profile_page(acc_token, ref_token):
    st.title("My profile")
    user_info = get_user_info(acc_token, ref_token)
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
    if st.button("Login confirm"):
        if password == password_confirm:
            res = signup(username, email, password)
            if res.get("id"):
                st.success(f"Success. Check email: {email} and verify")
            else:
                st.error(f"{res['detail']}")
        else:
            st.error("Password not match")


if __name__ == '__main__':
    access_token, refresh_token = load_token(FILE_NAME)


    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose action", ["SignUp", "Login", "Logout"])

    if page == "Login":
        if access_token:
            profile_page(access_token, refresh_token)
            access_token, refresh_token = load_token(FILE_NAME)
        else:
            access_token, refresh_token = login_page()

    elif page == "SignUp":
        if access_token:
            st.write("You are already in. Press Logout for SignUp")
        else:
            signup_page()

    if access_token:
        if st.button("Logout"):
            access_token, refresh_token = None, None
            save_token(access_token, refresh_token)

    save_token(access_token, refresh_token)

