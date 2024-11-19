import json
import os

ADMIN_SESSION_FILE = "admin_session.json"

def set_admin_session(admin_data):
    try:
        print("Setting session data:", admin_data)  # Debugging print
        with open(ADMIN_SESSION_FILE, "w") as file:
            json.dump(admin_data, file)
        print(f"Session data written to {ADMIN_SESSION_FILE}.")
    except Exception as e:
        print(f"Error writing session data: {e}")


def get_admin_session():
    if os.path.exists(ADMIN_SESSION_FILE):
        print("Session file exists.")
        try:
            with open(ADMIN_SESSION_FILE, "r") as file:
                data = json.load(file)
                print("Loaded session data:", data)  # Debugging print
                return data
        except json.JSONDecodeError:
            print("Error: Session file is corrupted.")
    print("No session file found.")
    return None
