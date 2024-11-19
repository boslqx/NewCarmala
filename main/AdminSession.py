import json
import os

# Ensure the file is created in the correct directory
ADMIN_SESSION_FILE = os.path.join(os.getcwd(), "admin_session.json")  # Current working directory

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

# Test Code
if __name__ == "__main__":
    # Test: Setting session
    admin_data = {"admin_id": 3, "username": "admin3", "role": "admin"}
    set_admin_session(admin_data)

    # Test: Getting session
    session_data = get_admin_session()
    if session_data:
        print(f"Admin ID: {session_data['admin_id']}, Username: {session_data['username']}")
    else:
        print("No session found.")
