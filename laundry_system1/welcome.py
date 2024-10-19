import tkinter as tk

def show_welcome_screen(username, proceed_callback):
    welcome_window = tk.Toplevel()  # Use Toplevel instead of Tk to avoid creating a new main window
    welcome_window.title("Welcome")
    welcome_window.geometry("300x200")

    tk.Label(welcome_window, text=f"Welcome, {username}!", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(welcome_window, text="Proceed to Main Menu", command=lambda: [welcome_window.destroy(), proceed_callback()]).pack(pady=20)
