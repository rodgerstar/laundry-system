import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk

import pandas as pd
from PIL import Image, ImageTk

import visualizing_data
from collecting_data import record_activity
from reporting import generate_report

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
        json.dump(users, file, indent=4)

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class LaundryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Laundry Management System")
        self.root.geometry("600x500")
        self.root.configure(bg="#ecf0f1")

        # Load loading icon
        self.loading_icon = self.load_image(r"C:\Users\Admin\Downloads\loading animation.webp")

        self.main_menu_frame = None
        self.show_login_screen()

    def load_image(self, file_name):
        try:
            image = Image.open(file_name)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def show_loading_screen(self):
        self.clear_window()
        loading_frame = tk.Frame(self.root, bg="#ecf0f1")
        loading_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(loading_frame, text="Loading...", font=("Helvetica", 18), bg="#ecf0f1").pack(pady=10)
        if self.loading_icon:
            tk.Label(loading_frame, image=self.loading_icon, bg="#ecf0f1").pack(pady=20)

        self.root.update()

    def hide_loading_screen(self):
        self.clear_window()

    def show_login_screen(self):
        self.show_loading_screen()
        self.root.after(1000, self._create_login_screen)

    def _create_login_screen(self):
        self.hide_loading_screen()
        LoginFrame(self.root, self).pack(expand=True, fill=tk.BOTH)

    def create_main_menu(self):
        self.show_loading_screen()
        self.root.after(1000, self._create_main_menu)

    def _create_main_menu(self):
        self.hide_loading_screen()
        MainMenuFrame(self.root, self).pack(expand=True, fill=tk.BOTH)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def record_activity(self):
        self.show_loading_screen()
        self.root.after(1000, self._record_activity)

    def _record_activity(self):
        self.hide_loading_screen()
        RecordActivityFrame(self.root, self).pack(expand=True, fill=tk.BOTH)

    def generate_report(self):
        self.show_loading_screen()
        self.root.after(1000, self._generate_report)

    def _generate_report(self):
        self.hide_loading_screen()
        try:
            generate_report()
            with open('csv_report_summary.txt', 'r') as f:
                report_content = f.read()
            self.display_report(report_content)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the report: {e}")

    def display_report(self, report_content):
        report_window = tk.Toplevel(self.root)
        report_window.title("Generated Report")
        report_window.geometry("600x400")
        report_window.configure(bg="#ecf0f1")

        text_widget = tk.Text(report_window, wrap=tk.WORD, padx=10, pady=10, bg="#bdc3c7", fg="#2c3e50")
        text_widget.insert(tk.END, report_content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)

        tk.Button(report_window, text="Close", command=report_window.destroy, bg="#e74c3c", fg="white").pack(pady=10)

    def visualize_data(self):
        self.show_loading_screen()
        self.root.after(1000, self._visualize_data)

    def _visualize_data(self):
        self.hide_loading_screen()
        try:
            period = simpledialog.askstring("Visualization", "Enter the period for visualization (daily/weekly/monthly/yearly):")
            if period:
                df = pd.read_csv('cleaned_customers_data.csv')
                visualizing_data.visualize_data(df, period)
                messagebox.showinfo("Success", "Data visualization successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while visualizing data: {e}")

    def exit_app(self):
        self.root.quit()

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#ecf0f1", padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Login", font=("Helvetica", 24), bg="#ecf0f1").pack(pady=20)

        tk.Label(self, text="Username:", bg="#ecf0f1").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:", bg="#ecf0f1").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login, bg="#3498db", fg="white").pack(pady=10)
        tk.Button(self, text="Sign Up", command=self.sign_up, bg="#2ecc71", fg="white").pack(pady=10)

    def login(self):
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()
        users = load_users()

        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Login successful!")
            self.app.create_main_menu()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def sign_up(self):
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get()
        users = load_users()

        if username in users:
            messagebox.showwarning("Sign Up", "Username already exists.")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Sign Up", "Sign up successful! You can now log in.")
            self.app.create_main_menu()

class MainMenuFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#ecf0f1", padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Bordered frame for the main menu
        frame = tk.Frame(self, bg="#bdc3c7", bd=2, relief="solid", padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Main Menu", font=("Helvetica", 24), bg="#bdc3c7").pack(pady=20)

        tk.Button(frame, text="Record Activity", command=self.app.record_activity, bg="#3498db", fg="white").pack(pady=10, anchor="w")
        tk.Button(frame, text="Generate Report", command=self.app.generate_report, bg="#2ecc71", fg="white").pack(pady=10, anchor="w")
        tk.Button(frame, text="Visualize Data", command=self.app.visualize_data, bg="#e67e22", fg="white").pack(pady=10, anchor="w")
        tk.Button(frame, text="Exit", command=self.app.exit_app, bg="#e74c3c", fg="white").pack(pady=10, anchor="w")

class RecordActivityFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#ecf0f1", padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Full-page bordered frame for data recording
        frame = tk.Frame(self, bg="#bdc3c7", bd=2, relief="solid", padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(frame, text="Record Activity", font=("Helvetica", 24), bg="#bdc3c7").pack(pady=20)

        tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#bdc3c7").pack(pady=5)
        self.date_entry = tk.Entry(frame)
        self.date_entry.pack(pady=5)

        tk.Label(frame, text="Customer Name:", bg="#bdc3c7").pack(pady=5)
        self.customer_name_entry = tk.Entry(frame)
        self.customer_name_entry.pack(pady=5)

        tk.Label(frame, text="Service:", bg="#bdc3c7").pack(pady=5)
        self.service_combobox = ttk.Combobox(frame, values=["Duvet/Blanket", "Clothes", "Dry Cleaning", "Ironing"])
        self.service_combobox.pack(pady=5)

        tk.Label(frame, text="Size:", bg="#bdc3c7").pack(pady=5)
        self.size_combobox = ttk.Combobox(frame, values=["Small", "Medium", "Large"])
        self.size_combobox.pack(pady=5)

        tk.Label(frame, text="Amount Paid:", bg="#bdc3c7").pack(pady=5)
        self.amount_paid_entry = tk.Entry(frame)
        self.amount_paid_entry.pack(pady=5)

        tk.Button(frame, text="Record", command=self.record, bg="#3498db", fg="white").pack(pady=10)

    def record(self):
        date = self.date_entry.get()
        customer_name = self.customer_name_entry.get().strip()
        service = self.service_combobox.get().strip()
        size = self.size_combobox.get().strip()
        amount_paid = self.amount_paid_entry.get().strip()

        if not validate_date(date):
            messagebox.showerror("Error", "Invalid date format. Please enter the date in YYYY-MM-DD format.")
            return

        if not customer_name or not service or not size or not amount_paid:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            amount_paid = float(amount_paid)
            record_activity(date, customer_name, service, size, amount_paid)
            messagebox.showinfo("Success", "Activity recorded successfully!")
            self.app.create_main_menu()
        except ValueError:
            messagebox.showerror("Error", "Amount paid must be a number.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LaundryManagementApp(root)
    root.mainloop()
