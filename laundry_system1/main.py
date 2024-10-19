import pandas as pd
from collecting_data import record_activity
from training import train_model  # Import the train_model function
from reporting import generate_report
import visualizing_data

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Record Daily Activity")
        print("2. Generate Report")
        print("3. Visualize Data")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            record_activity()
            print("Training model with the new data...")
            train_model()  # Automatically train the model after recording activity
            print("Model training completed successfully.")
        elif choice == '2':
            generate_report()
        elif choice == '3':
            visualize_data_menu()
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def visualize_data_menu():
    while True:
        try:
            df = pd.read_csv('cleaned_customers_data.csv')
            period = input("Enter the period for visualization (daily/weekly/monthly/yearly) or 'b' to go back: ").strip().lower()

            if period == 'b':
                return  # Go back to the main menu
            elif period not in ['daily', 'weekly', 'monthly', 'yearly']:
                print("Invalid period. Please choose from 'daily', 'weekly', 'monthly', or 'yearly'.")
            else:
                if period == 'daily':
                    start_date = input("Enter the start date (YYYY-MM-DD) or 'b' to go back: ").strip()
                    if start_date == 'b':
                        continue
                    end_date = input("Enter the end date (YYYY-MM-DD) or 'b' to go back: ").strip()
                    if end_date == 'b':
                        continue
                    visualizing_data.visualize_data(df, period, start_date=start_date, end_date=end_date)
                else:
                    # For weekly, monthly, and yearly, no specific date input is required
                    visualizing_data.visualize_data(df, period)

        except Exception as e:
            print(f"An error occurred while visualizing the data: {e}")

if __name__ == "__main__":
    main_menu()
