import json
import pickle
import configparser

import requests

config = configparser.ConfigParser()
config.read("config.ini")

FILE_NAME = config.get("DEV", "token_name")
SERVER_URL = config.get("DEV", "app_url")


def load_token(filename=FILE_NAME):
    try:
        with open(FILE_NAME, "rb") as fh:
            result = pickle.load(fh)
        # result = get_refresh_token(result[1])
        return result
    except IOError:
        with open(FILE_NAME, "wb") as fh:
            pickle.dump((None, None), fh)


def save_token(acc_token, ref_token):
    with open(FILE_NAME, "wb") as fh:
        pickle.dump((acc_token, ref_token), fh)


def login(username, password):
    data = {"username": username, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/login", data=data)
    if response.status_code == 200:
        return response.json()["access_token"], response.json()["refresh_token"]
    elif response.json().get("detail") == "Email not confirmed":
        return "Email not confirmed"
    else:
        return None


def signup(username, email, password):
    data = {"username": username, "email": email, "password": password}
    response = requests.post(f"{SERVER_URL}/api/auth/signup", data=json.dumps(data))
    return response.json()


def get_user_info(acc_token, ref_token):
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        return response.json()
    acc_token, ref_token = get_refresh_token(ref_token)
    headers = {"Authorization": f"Bearer {acc_token}"}
    response = requests.get(f"{SERVER_URL}/api/users/me/", headers=headers)
    if response.status_code == 200:
        save_token(acc_token, ref_token)
        return response.json()
    return None, None


def get_refresh_token(ref_token):
    headers = {"Authorization": f"Bearer {ref_token}"}
    response = requests.get(f"{SERVER_URL}/api/auth/refresh_token", headers=headers)
    if response.json().get("access_token"):
        return response.json()["access_token"], response.json()["refresh_token"]
    return None, None


def set_new_pass(pass_token, password, password_confirm):
    data = {"reset_password_token": pass_token, "new_password": password, "confirm_password": password_confirm}
    response = requests.post(f"{SERVER_URL}/api/auth/set_new_password", data=json.dumps(data))
    if response.status_code == 200:
        return response
    return response


def request_email(email_):
    data = {"email": email_}
    response = requests.post(f"{SERVER_URL}/api/auth/request_email", data=json.dumps(data))
    print(response.json())
    return response.json()


def reset_password(email):
    data = {"email": email}
    response = requests.post(f"{SERVER_URL}/api/auth/reset_password", data=json.dumps(data))
    print(response.json())
    return response.json()


def set_avatar(acc_token, data):

    headers = {"Authorization": f"Bearer {acc_token}"}
    files = {'file': data}
    response = requests.patch(f"{SERVER_URL}/api/users/avatar", files=files, headers=headers)
    return response.json()
