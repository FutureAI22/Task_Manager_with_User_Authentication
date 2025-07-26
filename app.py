import os
import hashlib
import json

# --- Constants ---
USERS_FILE = 'users.json'
TASKS_DIR = 'tasks' # Directory to store user-specific task files

# --- Helper Functions for File Handling ---
def load_users():
    """Loads user credentials from users.json."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Saves user credentials to users.json."""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def get_user_tasks_file(username):
    """Returns the path to the user's task file."""
    if not os.path.exists(TASKS_DIR):
        os.makedirs(TASKS_DIR)
    return os.path.join(TASKS_DIR, f"{username}_tasks.json")

def load_tasks(username):
    """Loads tasks for a specific user."""
    tasks_file = get_user_tasks_file(username)
    if not os.path.exists(tasks_file):
        return []
    with open(tasks_file, 'r') as f:
        return json.load(f)

def save_tasks(username, tasks):
    """Saves tasks for a specific user."""
    tasks_file = get_user_tasks_file(username)
    with open(tasks_file, 'w') as f:
        json.dump(tasks, f, indent=4)

def hash_password(password):
    """Hashes a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

# --- User Authentication Functions ---
def register_user():
    """Handles user registration."""
    users = load_users()
    while True:
        username = input("Enter new username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if username in users:
            print("Username already exists. Please choose a different one.")
        else:
            break
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty. Registration failed.")
        return False

    users[username] = hash_password(password)
    save_users(users)
    print("Registration successful!")
    return True

def login_user():
    """Handles user login."""
    users = load_users()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    if username in users and users[username] == hash_password(password):
        print(f"Welcome, {username}!")
        return username
    else:
        print("Invalid username or password.")
        return None

# --- Task Management Functions ---
def add_task(current_user):
    """Prompts user for a task description and adds it."""
    tasks = load_tasks(current_user)
    description = input("Enter task description: ").strip()
    if not description:
        print("Task description cannot be empty.")
        return

    # Generate a unique task ID (simple increment for now)
    task_id = 1 if not tasks else max(task['id'] for task in tasks) + 1
    new_task = {
        'id': task_id,
        'description': description,
        'status': 'Pending'
    }
    tasks.append(new_task)
    save_tasks(current_user, tasks)
    print(f"Task '{description}' (ID: {task_id}) added successfully.")

def view_tasks(current_user):
    """Displays all tasks for the logged-in user."""
    tasks = load_tasks(current_user)
    if not tasks:
        print("No tasks found.")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}")
    print("------------------\n")

def mark_task_completed(current_user):
    """Allows user to mark a task as completed by ID."""
    tasks = load_tasks(current_user)
    if not tasks:
        print("No tasks to mark as completed.")
        return

    view_tasks(current_user) # Show tasks to help user choose
    try:
        task_id = int(input("Enter the ID of the task to mark as completed: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    found = False
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'Completed'
            found = True
            break
    
    if found:
        save_tasks(current_user, tasks)
        print(f"Task ID {task_id} marked as Completed.")
    else:
        print(f"Task with ID {task_id} not found.")

def delete_task(current_user):
    """Allows user to delete a task by ID."""
    tasks = load_tasks(current_user)
    if not tasks:
        print("No tasks to delete.")
        return

    view_tasks(current_user) # Show tasks to help user choose
    try:
        task_id = int(input("Enter the ID of the task to delete: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    initial_len = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(tasks) < initial_len:
        save_tasks(current_user, tasks)
        print(f"Task ID {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

# --- Main Application Logic ---
def main_menu(current_user):
    """Displays the main task management menu."""
    while True:
        print("\n--- Task Manager Menu ---")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_task(current_user)
        elif choice == '2':
            view_tasks(current_user)
        elif choice == '3':
            mark_task_completed(current_user)
        elif choice == '4':
            delete_task(current_user)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def run_app():
    """Main function to run the Task Manager application."""
    current_user = None
    while current_user is None:
        print("\n--- Welcome to Task Manager ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        auth_choice = input("Enter your choice: ").strip()

        if auth_choice == '1':
            current_user = login_user()
        elif auth_choice == '2':
            register_user()
        elif auth_choice == '3':
            print("Exiting application. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")
    
    if current_user:
        main_menu(current_user)
        # After main_menu exits (user logged out), loop back to login/register

if __name__ == "__main__":
    run_app()
