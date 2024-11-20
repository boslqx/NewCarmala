import json
import os

# File to store the session
ADMIN_SESSION_FILE = os.path.join(os.getcwd(), "admin_session.json")


def set_admin_session(admin_data):
    """Sets the admin session data in a file."""
    try:
        print("[DEBUG] Setting session data:", admin_data)
        with open(ADMIN_SESSION_FILE, "w") as file:
            json.dump(admin_data, file)
        print(f"[DEBUG] Session data written to {ADMIN_SESSION_FILE}.")
    except Exception as e:
        print(f"[ERROR] Error writing session data: {e}")


def get_admin_session():
    """Gets the current admin session data."""
    if os.path.exists(ADMIN_SESSION_FILE):
        print("[DEBUG] Session file exists.")
        try:
            with open(ADMIN_SESSION_FILE, "r") as file:
                data = json.load(file)
                print("[DEBUG] Loaded session data:", data)
                return data
        except json.JSONDecodeError:
            print("[ERROR] Session file is corrupted.")
    print("[DEBUG] No session file found.")
    return None








