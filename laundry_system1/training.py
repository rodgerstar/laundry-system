import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

def train_model(data_path='cleaned_customers_data.csv'):
    # Load and preprocess data
    if not os.path.isfile(data_path):
        print(f"Data file '{data_path}' not found.")
        return

    df = pd.read_csv(data_path)

    # Check for and handle missing values
    if df.isnull().sum().any():
        print("Missing values detected. Handling missing values...")
        df.ffill(inplace=True)  # Forward fill

    # Feature engineering
    df['Date'] = pd.to_datetime(df['Date'])
    df['Day'] = df['Date'].dt.day
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Convert categorical features to numerical
    df['Service'] = df['Service'].astype('category')
    df['Customer Gender'] = df['Customer Gender'].astype('category')
    df['Customer Location'] = df['Customer Location'].astype('category')

    # Define features and target
    X = df[['Day', 'Month', 'Year', 'Service', 'Size', 'Customer Gender', 'Customer Location']]
    y = df['Total Amount']

    # Preprocessing and model pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False),
             ['Service', 'Size', 'Customer Gender', 'Customer Location']),
            ('num', StandardScaler(), ['Day', 'Month', 'Year'])
        ])

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])

    # Define parameter grid for hyperparameter tuning
    param_grid = {
        'regressor__n_estimators': [100, 200],
        'regressor__max_depth': [None, 10, 20],
        'regressor__min_samples_split': [2, 5],
        'regressor__min_samples_leaf': [1, 4]
    }

    # Implement GridSearchCV for hyperparameter tuning
    grid_search = GridSearchCV(pipeline, param_grid, cv=5,
                               scoring='neg_mean_squared_error', n_jobs=-1)
    grid_search.fit(X, y)

    # Best model from GridSearchCV
    best_model = grid_search.best_estimator_

    # Save the encoder
    preprocessor = best_model.named_steps['preprocessor']
    encoder = preprocessor.named_transformers_['cat']
    joblib.dump(encoder, 'encoder.pkl')

    # Save the model
    joblib.dump(best_model, 'model.pkl')

    # Cross-validation scores
    try:
        scores = cross_val_score(best_model, X, y, cv=5,
                                 scoring='neg_mean_squared_error')
        print(f'Cross-Validation MSE Scores: {-scores}')
        print(f'Average Cross-Validation MSE: {-scores.mean()}')
    except ValueError as e:
        print(f"Error during cross-validation: {e}")

    # Train/test split and evaluate
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42)
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)
    print(f'Mean Squared Error: {mean_squared_error(y_test, y_pred)}')
    print(f'R^2 Score: {r2_score(y_test, y_pred)}')

    print("Model trained and saved successfully!")


def update_data_and_train(new_data):
    # Check if the CSV file exists
    if os.path.isfile('cleaned_customers_data.csv'):
        df = pd.read_csv('cleaned_customers_data.csv')
    else:
        df = pd.DataFrame(columns=new_data.keys())

    # Append new data
    df = df.append(new_data, ignore_index=True)

    # Save the updated DataFrame back to CSV
    df.to_csv('cleaned_customers_data.csv', index=False)

    # Train the model with the updated data
    train_model()

if __name__ == "__main__":
    train_model()
