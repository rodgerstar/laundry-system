import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store user credentials
CREDENTIALS_FILE = "user_credentials.json"

# Load user credentials from the file
def load_users():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user credentials to the file
def save_users(users):
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(users, file)

# Show login screen
def show_login_screen(on_success):
    users = load_users()

    def attempt_login():
        username = entry_username.get()
        password = entry_password.get()

        if username in users and users[username] == password:
            messagebox.showinfo("Login Success", f"Welcome back, {username}!")
            login_window.destroy()
            on_success(username)  # Call the callback with the username
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def open_signup():
        login_window.destroy()  # Close login window before opening sign-up
        show_signup_screen(on_success)  # Pass the on_success callback to the sign-up screen

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#f0f0f0")

    tk.Label(login_window, text="Welcome to Laundry Management System", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)
    tk.Label(login_window, text="Please Login", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

    tk.Label(login_window, text="Username", bg="#f0f0f0").pack(pady=5)
    entry_username = tk.Entry(login_window)
    entry_username.pack(pady=5)

    tk.Label(login_window, text="Password", bg="#f0f0f0").pack(pady=5)
    entry_password = tk.Entry(login_window, show="*")
    entry_password.pack(pady=5)

    tk.Button(login_window, text="Login", command=attempt_login, bg="#4CAF50", fg="white").pack(pady=15)
    tk.Button(login_window, text="Sign Up", command=open_signup, bg="#008CBA", fg="white").pack(pady=5)

    login_window.mainloop()

# Show sign-up screen
def show_signup_screen(on_success):
    users = load_users()

    def attempt_signup():
        username = entry_new_username.get()
        password = entry_new_password.get()

        if username in users:
            messagebox.showerror("Sign Up Failed", "Username already exists")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Sign Up Success", "Account created successfully!")
            signup_window.destroy()
            show_login_screen(on_success)  # Re-open login screen after successful sign-up

    signup_window = tk.Tk()
    signup_window.title("Sign Up")
    signup_window.geometry("400x300")
    signup_window.configure(bg="#f0f0f0")

    tk.Label(signup_window, text="Create a New Account", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    tk.Label(signup_window, text="New Username", bg="#f0f0f0").pack(pady=5)
    entry_new_username = tk.Entry(signup_window)
    entry_new_username.pack(pady=5)

    tk.Label(signup_window, text="New Password", bg="#f0f0f0").pack(pady=5)
    entry_new_password = tk.Entry(signup_window, show="*")
    entry_new_password.pack(pady=5)

    tk.Button(signup_window, text="Sign Up", command=attempt_signup, bg="#4CAF50", fg="white").pack(pady=20)

    signup_window.mainloop()
