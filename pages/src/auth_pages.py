import streamlit as st

from pages.src.auth_services import login, signup
from pages.src.auth_services import get_user_info, set_new_pass, set_avatar
from pages.src.auth_services import reset_password, request_email

IMG_TYPE = ['png', 'jpg', 'jpeg', 'gif', 'svg']


def login_page():
    acc_token, ref_token = None, None
    st.title("Login")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = login(username, password)
        if type(res) == tuple:
            acc_token, ref_token = res
            st.success("Success.")
            # profile_page(acc_token, ref_token)
            return acc_token, ref_token
        elif type(res) == str:
            st.text("Email is not confirmed.")
        else:
            st.error("Wrong username or password")
    return None, None


def change_avatar_page(acc_token, ref_token):
    new_avatar = st.file_uploader("Upload your image here and click on 'Process'", type=IMG_TYPE)
    if new_avatar:
        if st.button("Process"):
            with st.spinner("Processing"):
                res = set_avatar(acc_token, new_avatar.getvalue())
                if res.get("avatar"):
                    st.success("Avatar update successfully.")
                else:
                    st.error(f"Error: {res}")


def request_mail_page():
    st.title("Resending email signup confirmation")
    email_reset = st.text_input("Email request")
    if st.button("Request email"):
        request_email(email_reset)
        st.success(f"Success.  Check email: {email_reset} and verify")


def reset_password_page():
    st.title("Reset password via email")
    email_reset = st.text_input("Email for reset password")
    if st.button("Reset password"):
        print(reset_password(email_reset))
        st.success(f"Success.  Check email: {email_reset}")
    pass_token = st.text_input("Paste token from email")
    password = st.text_input("New password", type="password")
    password_confirm = st.text_input("Confirm new password", type="password")
    if st.button("Reset confirm"):
        if password == password_confirm:
            res = set_new_pass(pass_token, password, password_confirm)
            if res:
                st.success(f"{res}")
            else:
                st.error(f"Something wrong.")
        else:
            st.error("Password not match")


def start_page():
    st.title("Login for use all features")


def profile_page(acc_token, ref_token):
    st.title("My profile")
    user_info = get_user_info(acc_token, ref_token)
    if user_info:
        st.write(f"Username: {user_info['username']}")
        st.write(f"Email: {user_info['email']}")
        st.image(f"{user_info['avatar']}")
    else:
        st.error("Unable connect")


def signup_page():
    st.title("SignUp")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    password_confirm = st.text_input("Confirm password", type="password")
    if st.button("SignUp confirm"):
        if password == password_confirm:
            res = signup(username, email, password)
            if res.get("id"):
                st.success(f"Success. Check email: {email} and verify")
            else:
                st.error(f"{res['detail']}")
        else:
            st.error("Password not match")
