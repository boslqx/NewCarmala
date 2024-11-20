import json
import os

SESSION_FILE = "session.json"
ADMIN_SESSION_FILE = "AdminSession.json"

# Function to get the admin session
def get_admin_session():
    """
    Retrieves the current admin session from the session file.
    """
    if os.path.exists(ADMIN_SESSION_FILE):
        with open(ADMIN_SESSION_FILE, "r") as file:
            try:
                session_data = json.load(file)
                print(f"[DEBUG] Admin session data loaded: {session_data}")  # Debugging output
                return session_data
            except json.JSONDecodeError:
                print("[ERROR] Admin session file is corrupted.")
                return None
    print("[DEBUG] No admin session found.")  # Debugging output
    return None  # No session found

# Function to set the admin session
def set_admin_session(admin_data):
    """
    Saves the admin session to the session file.
    """
    try:
        with open(ADMIN_SESSION_FILE, "w") as file:
            json.dump(admin_data, file)
        print(f"[DEBUG] Admin session saved: {admin_data}")  # Debugging output
    except Exception as e:
        print(f"[ERROR] Failed to save admin session: {e}")  # Error handling

# Function to clear the admin session
def clear_admin_session():
    """
    Deletes the admin session file.
    """
    if os.path.exists(ADMIN_SESSION_FILE):
        os.remove(ADMIN_SESSION_FILE)
        print("[DEBUG] Admin session cleared.")

# Function to set the user session
def set_user_session(user_data):
    """
    Saves the user session to the session file.
    """
    try:
        with open(SESSION_FILE, "w") as file:
            json.dump(user_data, file)
        print(f"[DEBUG] User session saved: {user_data}")  # Debugging output
    except Exception as e:
        print(f"[ERROR] Failed to save user session: {e}")  # Error handling

# Function to get the user session
def get_user_session():
    """
    Retrieves the current user session from the session file.
    """
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as file:
            try:
                session_data = json.load(file)
                print(f"[DEBUG] User session data loaded: {session_data}")  # Debugging output
                return session_data
            except json.JSONDecodeError:
                print("[ERROR] User session file is corrupted.")
                return None
    print("[DEBUG] No user session found.")  # Debugging output
    return None  # No session found

# Function to clear the user session
def clear_user_session():
    """
    Deletes the user session file.
    """
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        print("[DEBUG] User session cleared.")
