import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

def visualize_data(df, period='daily', start_date=None, end_date=None):
    try:
        # Convert to datetime and filter by date range
        df['Date'] = pd.to_datetime(df['Date'])
        df['Total Amount'] = df['Total Amount'].astype(float)

        if start_date and end_date:
            df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        check_columns(df)  # Check for missing columns

        # Group data by period
        df_grouped = group_by_period(df, period)

        # Visualizations
        plot_total_amount_over_time(df_grouped, period)
        plot_pie_chart(df['Service'], 'Service Distribution', 'service_distribution.png')
        plot_pie_chart(df.groupby('Customer Gender')['Total Amount'].sum(), 'Spending Distribution by Gender', 'spending_by_gender.png')
        plot_bar_chart(df, 'Service', 'Total Amount', 'Customer Gender', 'Total Amount of Services by Gender', 'services_by_gender.png')
        plot_bar_chart(df, df['Date'].dt.date, 'Total Amount', None, f'Total Amount Received Over Time ({period.capitalize()})', 'amount_received_over_time.png')
        plot_line_chart(df, 'Date', 'Total Amount', 'Customer Gender', f'Price Comparison Between Genders Over Time ({period.capitalize()})', 'price_comparison_genders.png')
        plot_location_distribution(df)

        # Predictions
        future_df = prepare_future_data(df)
        predict_and_plot(future_df)

        print("Data visualized and predictions displayed successfully!")
    except Exception as e:
        print(f"An error occurred while visualizing the data: {e}")

def check_columns(df):
    required_columns = {'Customer Location', 'Customer Gender', 'Service', 'Size', 'Date', 'Day', 'Month', 'Year'}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise ValueError(f"Columns are missing: {missing_columns}")

def group_by_period(df, period):
    if period == 'daily':
        return df.groupby(df['Date'].dt.date)['Total Amount'].sum()
    elif period == 'weekly':
        return df.groupby(df['Date'].dt.to_period('W').apply(lambda r: r.start_time))['Total Amount'].sum()
    elif period == 'monthly':
        return df.groupby(df['Date'].dt.to_period('M').apply(lambda r: r.start_time))['Total Amount'].sum()
    else:
        raise ValueError("Invalid period specified. Choose from 'daily', 'weekly', or 'monthly'.")

def plot_total_amount_over_time(df_grouped, period):
    plt.figure(figsize=(12, 6))
    plt.plot(df_grouped.index, df_grouped.values, marker='o', linestyle='-')
    plt.title(f'Total Amount of Services Over Time ({period.capitalize()})')
    plt.xlabel('Date')
    plt.ylabel('Total Amount')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('total_amount_over_time.png')
    plt.show()

def plot_pie_chart(data, title, filename):
    plt.figure(figsize=(8, 8))
    data.value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.ylabel('')
    plt.savefig(filename)
    plt.show()

def plot_bar_chart(df, x, y, hue, title, filename):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, hue=hue, data=df, estimator=sum, errorbar=None)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.savefig(filename)
    plt.show()

def plot_line_chart(df, x, y, hue, title, filename):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=df[x].dt.date, y=y, hue=hue, data=df, estimator=sum, errorbar=None)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.savefig(filename)
    plt.show()

def plot_location_distribution(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Customer Location', order=df['Customer Location'].value_counts().index)
    plt.title('Location Distribution')
    plt.xlabel('Location')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.savefig('locations_served.png')
    plt.show()

def prepare_future_data(df):
    model = joblib.load('model.pkl')
    encoder = joblib.load('encoder.pkl')
    locations_df = pd.read_csv('cleaned_customers_data.csv')
    locations = locations_df['Customer Location'].unique()

    future_dates = pd.date_range(start=df['Date'].max(), periods=30)
    future_data = pd.DataFrame({'Date': future_dates})
    future_data['Day'] = future_data['Date'].dt.day
    future_data['Month'] = future_data['Date'].dt.month
    future_data['Year'] = future_data['Date'].dt.year

    service_types = df['Service'].unique()
    sizes = ['Small', 'Medium', 'Large']
    genders = df['Customer Gender'].unique()

    prediction_data = [
        {'Date': future_dates[0], 'Day': future_data['Day'].iloc[0], 'Month': future_data['Month'].iloc[0],
         'Year': future_data['Year'].iloc[0], 'Service': service, 'Size': size, 'Customer Gender': gender,
         'Customer Location': location}
        for service in service_types
        for size in sizes
        for gender in genders
        for location in locations
    ]

    future_df = pd.DataFrame(prediction_data)

    feature_names = encoder.get_feature_names_out()
    future_df = pd.get_dummies(future_df, columns=['Service', 'Size', 'Customer Gender', 'Customer Location'])
    missing_cols = set(feature_names) - set(future_df.columns)
    for col in missing_cols:
        future_df[col] = 0

    return future_df[feature_names]

def predict_and_plot(future_df):
    model = joblib.load('model.pkl')
    predictions = model.predict(future_df)
    future_df['Predicted Amount'] = predictions

    plt.figure(figsize=(12, 6))
    plt.plot(future_df['Date'], future_df['Predicted Amount'], marker='o', linestyle='-')
    plt.title('Predicted Demand Over the Next 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Predicted Amount')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('predicted_demand_30_days.png')
    plt.show()

def main():
    try:
        df = pd.read_csv('cleaned_customers_data.csv')
        period = input("Enter the period for visualization (daily/weekly/monthly): ").strip().lower()

        if period not in ['daily', 'weekly', 'monthly']:
            print("Invalid period. Please choose from 'daily', 'weekly', or 'monthly'.")
            return

        start_date = None
        end_date = None

        visualize_data(df, period, start_date, end_date)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
