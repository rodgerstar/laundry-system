import pandas as pd
import random
from datetime import datetime, timedelta

# Original data
data = {
    "Date": ["2024-08-15", "2024-08-15", "2024-08-15", "2024-08-16", "2024-08-16", "2024-08-17", "2024-08-17"],
    "Customer Name": ["John Doe", "Jane Smith", "Emily Brown", "Michael Johnson", "Susan Lee", "David Wilson",
                      "Linda Green"],
    "Customer Location": ["Nairobi", "Kisumu", "Mombasa", "Nairobi", "Meru", "Nyeri", "Thika"],
    "Customer Gender": ["Male", "Female", "Female", "Male", "Female", "Male", "Female"],
    "Service": ["Dry Cleaning", "Duvet/Blanket Cleaning", "Clothes Cleaning", "Duvet/Blanket Cleaning",
                "Clothes Cleaning", "Dry Cleaning", "Duvet/Blanket Cleaning"],
    "Size": ["", "Large", "Medium", "Small", "Large", "", "Medium"],
    "Total Amount": [500, 500, 400, 200, 600, 500, 350]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Set the start and end dates for the 3-4 month period
start_date = datetime(2024, 8, 18)  # Start after the last date in original data
end_date = datetime(2024, 12, 15)  # Roughly 4 months later

# Generate dates with 3-4 random days per week
all_dates = pd.date_range(start=start_date, end=end_date).tolist()
selected_dates = []

current_week = start_date
while current_week <= end_date:
    # Get all dates for the current week
    weekly_dates = [d for d in all_dates if d.isocalendar()[1] == current_week.isocalendar()[1]]

    # Only sample if there are enough days in the week, otherwise use all available days
    days_to_sample = min(len(weekly_dates), random.randint(3, 4))

    if days_to_sample > 0:
        selected_dates.extend(random.sample(weekly_dates, days_to_sample))

    current_week += timedelta(days=7)

# Generate a list of unique customers
unique_customers = ["John Doe", "Jane Smith", "Emily Brown", "Michael Johnson", "Susan Lee", "David Wilson",
                    "Linda Green",
                    "Anna White", "Chris Martin", "Sarah Parker", "James Black", "Laura King", "Henry Adams",
                    "Fiona Blake", "George Hall", "Amy Young", "Peter Stone", "Rachel Green", "Sam Harris",
                    "Lucy Clarke", "Oscar Bell", "Nina Roberts", "Tom Wright", "Emma Scott", "Nick Hughes"]

# Ensure the number of customers doesn't exceed the available unique customers
num_customers = min(len(unique_customers), random.randint(25, 40))
customers = random.sample(unique_customers, num_customers)

# Simulate customer data
genders = ["Male", "Female"]
services = ["Dry Cleaning", "Duvet/Blanket Cleaning", "Clothes Cleaning"]
sizes = ["", "Small", "Medium", "Large"]

# The specified locations for customer activities
locations = ["Chuka Town", "Ndagani Market", "Lowlands", "Gate F", "Kibumbumbu", "Royals", "Marine", "Gate A",
             "Slaughter", "Tumaini"]

new_data = []

for date in selected_dates:
    # Choose a random number of customers for each day, allowing for repeats
    daily_customers = random.sample(customers, random.randint(1, 5))

    for customer in daily_customers:
        new_data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Customer Name": customer,
            "Customer Location": random.choice(locations),
            "Customer Gender": random.choice(genders),
            "Service": random.choice(services),
            "Size": random.choice(sizes),
            "Total Amount": random.randint(200, 800)  # Random amount between 200 and 800
        })

# Convert to DataFrame and concatenate with original data
df_extended = pd.DataFrame(new_data)
df_combined = pd.concat([df, df_extended], ignore_index=True)

# Save to CSV
df_combined.to_csv('extended_weekly_customers.csv', index=False)
print("Extended weekly CSV file created and populated successfully!")
