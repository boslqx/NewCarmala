import json
import os

SESSION_FILE = "session.json"

def set_user_session(user_data):
    with open(SESSION_FILE, "w") as file:
        json.dump(user_data, file)

def get_user_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            return json.load(file)
    return None  # If the file does not exist, no user is logged in

def clear_user_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
