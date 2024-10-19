import os
import pandas as pd

def read_csv_data():
    """Read and process data from cleaned_customers_data.csv."""
    csv_file = 'cleaned_customers_data.csv'

    if not os.path.exists(csv_file):
        print(f"The file '{csv_file}' does not exist.")
        return None

    try:
        data = pd.read_csv(csv_file)
        return data
    except Exception as e:
        print(f"Failed to read CSV file {csv_file}: {e}")
        return None

def generate_report():
    data = read_csv_data()

    if data is None or data.empty:
        print("No data found in the CSV file.")
        return

    with open('csv_report_summary.txt', 'w') as f:
        # Report Header
        f.write("Customer Data Report\n")
        f.write("=" * 50 + "\n")

        # Summary Statistics Table
        f.write("\nSummary Statistics:\n")
        f.write("=" * 50 + "\n")
        summary_stats = data.describe().to_string()
        f.write(summary_stats + "\n")
        f.write("=" * 50 + "\n")

        # Grouped Data (e.g., by location or gender)
        if 'location' in data.columns and 'amount' in data.columns:
            location_summary = data.groupby('location')['amount'].sum().to_string()
            f.write("\nTotal Amount by Location:\n")
            f.write("=" * 50 + "\n")
            f.write(location_summary + "\n")
            f.write("=" * 50 + "\n")

        if 'gender' in data.columns and 'amount' in data.columns:
            gender_summary = data.groupby('gender')['amount'].sum().to_string()
            f.write("\nTotal Amount by Gender:\n")
            f.write("=" * 50 + "\n")
            f.write(gender_summary + "\n")
            f.write("=" * 50 + "\n")

        # Top 5 Activities (based on amount)
        if 'activity' in data.columns and 'amount' in data.columns:
            top_activities = data.groupby('activity')['amount'].sum().sort_values(ascending=False).head(5).to_string()
            f.write("\nTop 5 Activities by Amount:\n")
            f.write("=" * 50 + "\n")
            f.write(top_activities + "\n")
            f.write("=" * 50 + "\n")

        # Sample Data Table
        f.write("\nSample Data:\n")
        f.write("=" * 50 + "\n")
        f.write(data.head().to_string())
        f.write("\n" + "=" * 50 + "\n")

    print("Report generated successfully!")
    print(f"Report saved to 'csv_report_summary.txt'")

def generate_ai_insights(data):
    """Generate AI-driven insights from the data."""
    insights = []

    # Example Insight: Check for high spenders
    if 'amount' in data.columns:
        high_spenders = data[data['amount'] > data['amount'].mean()]
        if not high_spenders.empty:
            insights.append(f"There are {len(high_spenders)} transactions with amounts higher than the average ({data['amount'].mean():.2f}).")

    # Example Insight: Gender-based spending
    if 'gender' in data.columns and 'amount' in data.columns:
        gender_spending = data.groupby('gender')['amount'].sum()
        insights.append(f"Gender-based spending: {gender_spending.to_dict()}")

    # Example Insight: Location-based spending
    if 'location' in data.columns and 'amount' in data.columns:
        location_spending = data.groupby('location')['amount'].sum()
        insights.append(f"Location-based spending: {location_spending.to_dict()}")

    return insights

if __name__ == "__main__":
    data = read_csv_data()
    if data is not None:
        generate_report()
        ai_insights = generate_ai_insights(data)
        print("\nAI-Driven Insights:")
        print("=" * 50)
        for insight in ai_insights:
            print(insight)
