import pandas as pd
from datetime import datetime
import os

def record_activity():
    print("\nEnter Daily Activity")

    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    customer_name = input("Enter customer's name: ").strip()
    customer_location = input("Enter customer's location: ").strip()

    while True:
        customer_gender = input("Enter customer's gender (Male/Female): ").strip().capitalize()
        if customer_gender in ["Male", "Female"]:
            break
        print("Invalid gender. Please enter 'Male' or 'Female'.")

    while True:
        service = input("Enter service type (Dry Cleaning, Duvet/Blanket Cleaning, Clothes Cleaning): ").strip().capitalize()
        service_dict = {
            "Dry cleaning": 500,
            "Duvet/blanket cleaning": ["Small", "Medium", "Large"],
            "Clothes cleaning": ["Small", "Medium", "Large"]
        }

        if service in service_dict:
            break
        print("Invalid service type. Please enter 'Dry Cleaning', 'Duvet/Blanket Cleaning', or 'Clothes Cleaning'.")

    if service == "Duvet/blanket cleaning":
        while True:
            size = input("Enter size (Small, Medium, Large): ").strip().capitalize()
            if size in service_dict[service]:
                amount = {"Small": 200, "Medium": 350, "Large": 500}[size]
                break
            print("Invalid size. Please enter 'Small', 'Medium', or 'Large'.")
    elif service == "Clothes cleaning":
        while True:
            size = input("Enter bin size (Small, Medium, Large): ").strip().capitalize()
            if size in service_dict[service]:
                amount = {"Small": 300, "Medium": 400, "Large": 600}[size]
                break
            print("Invalid bin size. Please enter 'Small', 'Medium', or 'Large'.")
    else:
        amount = 500

    while True:
        ironing = input("Was ironing included? (yes/no): ").strip().lower()
        if ironing in ["yes", "no"]:
            if ironing == "yes":
                amount += 200
            break
        print("Invalid input. Please enter 'yes' or 'no'.")

    activity = {
        "Date": date,
        "Customer Name": customer_name,
        "Customer Location": customer_location,
        "Customer Gender": customer_gender,
        "Service": service,
        "Total Amount": amount
    }

    df = pd.DataFrame([activity])

    file_exists = os.path.isfile('daily_activities.csv')

    try:
        df.to_csv('daily_activities.csv', mode='a', index=False, header=not file_exists)
        print("Activity recorded successfully!")
    except Exception as e:
        print(f"An error occurred while saving the activity: {e}")

if __name__ == "__main__":
    record_activity()
