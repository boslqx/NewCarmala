import json
import os

SESSION_FILE = "session.json"
Session_FILE = "AdminSession.json"

def get_admin_session():
    """
    Retrieves the current admin session from the session file.
    """
    if os.path.exists(Session_FILE):
        with open(Session_FILE, "r") as file:
            session_data = json.load(file)
            print(f"[DEBUG] Admin session data loaded: {session_data}")  # Debugging output
            return session_data
    print("[DEBUG] No admin session found.")  # Debugging output
    return None  # No session found

def set_admin_session(admin_data):
    """
    Saves the admin session to the session file.
    """
    try:
        with open(Session_FILE, "w") as file:
            json.dump(admin_data, file)
        print(f"[DEBUG] Admin session saved: {admin_data}")  # Debugging output
    except Exception as e:
        print(f"[ERROR] Failed to save admin session: {e}")  # Error handling


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
