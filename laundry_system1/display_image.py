import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from datetime import datetime
import json
import os
import pandas as pd
import visualizing_data
from collecting_data import record_activity
from training import train_model
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
        self.root.geometry("500x400")
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
        loading_window = self.show_loading_icon()
        self.root.after(1000, self._record_activity, loading_window)

    def _record_activity(self, loading_window):
        try:
            date_str = simpledialog.askstring("Record Activity", "Enter the date (YYYY-MM-DD):")
            if not date_str or not validate_date(date_str):
                messagebox.showwarning("Warning", "Invalid or missing date. Please use YYYY-MM-DD.")
                self.hide_loading_icon(loading_window)
                return

            customer_name = simpledialog.askstring("Record Activity", "Enter customer's name:").strip()
            customer_location = simpledialog.askstring("Record Activity", "Enter customer's location:").strip()
            customer_gender = simpledialog.askstring("Record Activity", "Enter customer's gender (Male/Female):").strip().capitalize()
            if customer_gender not in ["Male", "Female"]:
                messagebox.showwarning("Warning", "Invalid gender. Please enter 'Male' or 'Female'.")
                self.hide_loading_icon(loading_window)
                return

            service = simpledialog.askstring("Record Activity", "Enter service type (Dry Cleaning, Duvet/Blanket Cleaning, Clothes Cleaning):").strip().capitalize()
            service_dict = {
                "Dry Cleaning": 500,
                "Duvet/Blanket Cleaning": ["Small", "Medium", "Large"],
                "Clothes Cleaning": ["Small", "Medium", "Large"]
            }

            if service not in service_dict:
                messagebox.showwarning("Warning", "Invalid service type. Please enter 'Dry Cleaning', 'Duvet/Blanket Cleaning', or 'Clothes Cleaning'.")
                self.hide_loading_icon(loading_window)
                return

            if service in ["Duvet/Blanket Cleaning", "Clothes Cleaning"]:
                size = simpledialog.askstring("Record Activity", "Enter size (Small, Medium, Large):").strip().capitalize()
                if size not in service_dict[service]:
                    messagebox.showwarning("Warning", "Invalid size. Please enter 'Small', 'Medium', or 'Large'.")
                    self.hide_loading_icon(loading_window)
                    return
                amount = {"Small": 200, "Medium": 350, "Large": 500}[size] if service == "Duvet/Blanket Cleaning" else {"Small": 300, "Medium": 400, "Large": 600}[size]
            else:
                amount = 500

            ironing = simpledialog.askstring("Record Activity", "Was ironing included? (yes/no):").strip().lower()
            if ironing == "yes":
                amount += 200
            elif ironing != "no":
                messagebox.showwarning("Warning", "Invalid input for ironing. Please enter 'yes' or 'no'.")
                self.hide_loading_icon(loading_window)
                return

            record_activity(date_str, customer_name, customer_location, customer_gender, service, amount)
            train_model()  # Train model with the new data
            messagebox.showinfo("Success", "Activity recorded and model trained successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.hide_loading_icon(loading_window)

    def generate_report(self):
        loading_window = self.show_loading_icon()
        self.root.after(1000, self._generate_report, loading_window)

    def _generate_report(self, loading_window):
        try:
            generate_report()
            with open('csv_report_summary.txt', 'r') as f:
                report_content = f.read()
            self.display_report(report_content)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the report: {e}")
        finally:
            self.hide_loading_icon(loading_window)

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
        loading_window = self.show_loading_icon()
        self.root.after(1000, self._visualize_data, loading_window)

    def _visualize_data(self, loading_window):
        try:
            period = simpledialog.askstring("Visualization", "Enter the period for visualization (daily/weekly/monthly/yearly):")
            if period:
                df = pd.read_csv('cleaned_customers_data.csv')
                visualizing_data.visualize_data(df, period)
                messagebox.showinfo("Success", "Data visualization successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while visualizing data: {e}")
        finally:
            self.hide_loading_icon(loading_window)

    def show_loading_icon(self):
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Loading")
        loading_window.geometry("300x200")
        loading_window.configure(bg="#ecf0f1")

        tk.Label(loading_window, text="Loading...", font=("Helvetica", 18), bg="#ecf0f1").pack(pady=10)
        if self.loading_icon:
            tk.Label(loading_window, image=self.loading_icon, bg="#ecf0f1").pack(pady=20)

        return loading_window

    def hide_loading_icon(self, loading_window):
        loading_window.destroy()

    def exit_app(self):
        self.root.quit()

class LoginFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.configure(bg="#ecf0f1")
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = load_users()

        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Login successful!")
            self.app.create_main_menu()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def sign_up(self):
        username = self.username_entry.get()
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
        self.configure(bg="#ecf0f1")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Main Menu", font=("Helvetica", 24), bg="#ecf0f1").pack(pady=20)

        tk.Button(self, text="Record Activity", command=self.app.record_activity, bg="#3498db", fg="white").pack(pady=10)
        tk.Button(self, text="Generate Report", command=self.app.generate_report, bg="#2ecc71", fg="white").pack(pady=10)
        tk.Button(self, text="Visualize Data", command=self.app.visualize_data, bg="#e67e22", fg="white").pack(pady=10)
        tk.Button(self, text="Exit", command=self.app.exit_app, bg="#e74c3c", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LaundryManagementApp(root)
    root.mainloop()
