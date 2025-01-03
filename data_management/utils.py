import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np


def preprocess_dataset(file_path, missing_value_strategy='mean'):
    """
    Preprocess the dataset:
    - Handle missing values
    - Handle categorical and numeric columns
    - Scale numeric features
    - Encode categorical features
    - Return preprocessed features (X) and target (y)

    Args:
        file_path (str): Path to the CSV file.
        missing_value_strategy (str): Strategy for filling missing values ('mean', 'median', or 'constant').

    Returns:
        X_preprocessed (np.ndarray): Preprocessed feature matrix.
        y (pd.Series): Target variable.
    """
    # Load the dataset
    data = pd.read_csv(file_path)

    # Ensure 'Disease' column exists
    if "Disease" not in data.columns:
        raise ValueError("Dataset must contain a 'Disease' column.")

    # Separate features and target
    X = data.drop(columns=["Disease"])
    y = data["Disease"]

    # Identify numeric and categorical columns
    numeric_columns = X.select_dtypes(include=['number']).columns
    categorical_columns = X.select_dtypes(include=['object', 'category']).columns

    if len(numeric_columns) == 0 and len(categorical_columns) == 0:
        raise ValueError("Dataset contains no usable features (numeric or categorical).")

    # Define preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy=missing_value_strategy)),  # Handle missing values
        ('scaler', StandardScaler())  # Scale numeric features
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),  # Handle missing values
        ('onehot', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode categorical features
    ])

    # Combine transformations using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_columns),
            ('cat', categorical_transformer, categorical_columns)
        ]
    )

    # Apply preprocessing to the features
    X_preprocessed = preprocessor.fit_transform(X)

    # Log warnings if needed
    if X.isnull().sum().sum() > 0:
        print("Warning: Missing values were detected and handled.")

    if len(X.columns) > 50:
        print("Warning: The dataset has many features. Consider dimensionality reduction.")

    return X_preprocessed, y
