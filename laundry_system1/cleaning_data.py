import pandas as pd
import numpy as np

def clean_data(input_file, output_file):
    # Load the data
    df = pd.read_csv(input_file)

    # Feature extraction and cleaning
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Handling missing values with forward fill
    df = df.ffill()

    # Extracting and encoding variables
    df['Customer Gender'] = df['Customer Gender'].astype('category')
    df['Customer Location'] = df['Customer Location'].astype('category')
    df['Service'] = df['Service'].astype('category')
    df['Size'] = df['Size'].astype('category')

    # Gender correction for consistency
    gender_corrections = {
        'John Doe': 'Male', 'Jane Smith': 'Female', 'Emily Brown': 'Female', 'Michael Johnson': 'Male',
        'Susan Lee': 'Female', 'David Wilson': 'Male', 'Linda Green': 'Female', 'Lucy Clarke': 'Female',
        'Emma Scott': 'Female', 'Henry Adams': 'Male', 'Anna White': 'Female', 'Peter Stone': 'Male',
        'Fiona Blake': 'Female', 'Tom Wright': 'Male', 'Sarah Parker': 'Female', 'Oscar Bell': 'Male',
        'George Hall': 'Male', 'Rachel Green': 'Female', 'Amy Young': 'Female', 'Sam Harris': 'Male',
        'Laura King': 'Female', 'James Black': 'Male', 'Chris Martin': 'Male', 'Nick Hughes': 'Male',
        'Nina Roberts': 'Female'
    }
    df['Customer Gender'] = df['Customer Name'].map(gender_corrections).fillna(df['Customer Gender'])

    # Create columns for pricing
    df['Daily Price'] = df['Total Amount'] / (df['Date'].diff().dt.days.fillna(1).astype(int) + 1)
    df['Weekly Price'] = df['Total Amount'] / ((df['Date'].diff().dt.days.fillna(1).astype(int) // 7) + 1)
    df['Monthly Price'] = df['Total Amount'] / ((df['Date'].diff().dt.days.fillna(1).astype(int) // 30) + 1)

    # Replace negative and infinite prices with NaN for further handling
    df['Daily Price'] = df['Daily Price'].replace([np.inf, -np.inf], np.nan)
    df['Weekly Price'] = df['Weekly Price'].replace([np.inf, -np.inf], np.nan)
    df['Monthly Price'] = df['Monthly Price'].replace([np.inf, -np.inf], np.nan)
    df['Daily Price'] = df['Daily Price'].apply(lambda x: np.nan if x < 0 else x)
    df['Weekly Price'] = df['Weekly Price'].apply(lambda x: np.nan if x < 0 else x)
    df['Monthly Price'] = df['Monthly Price'].apply(lambda x: np.nan if x < 0 else x)

    # Fill missing prices with the mean value
    df['Daily Price'] = df['Daily Price'].fillna(df['Daily Price'].mean())
    df['Weekly Price'] = df['Weekly Price'].fillna(df['Weekly Price'].mean())
    df['Monthly Price'] = df['Monthly Price'].fillna(df['Monthly Price'].mean())

    # Counting the number of times each customer has been served
    df['Number of Times Served'] = df.groupby('Customer Name')['Customer Name'].transform('count')

    # Ensure required columns are included
    required_columns = ['Date', 'Day', 'Month', 'Year', 'Customer Name', 'Customer Gender',
                        'Customer Location', 'Service', 'Size', 'Daily Price', 'Weekly Price',
                        'Monthly Price', 'Total Amount', 'Number of Times Served']
    for col in required_columns:
        if col not in df.columns:
            df[col] = np.nan  # Add missing columns with NaN values

    # Save the cleaned data
    df_cleaned = df[required_columns]
    df_cleaned.to_csv(output_file, index=False)
    print(f"Data cleaned and saved to {output_file}")

if __name__ == "__main__":
    input_file = 'extended_weekly_customers.csv'
    output_file = 'cleaned_customers_data.csv'
    clean_data(input_file, output_file)
