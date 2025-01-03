import os  # Import for directory handling
import joblib
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from data_management.models import Dataset
from data_management.utils import preprocess_dataset  # Import preprocessing function

def train_model(request):
    # Load the latest uploaded dataset
    latest_dataset = Dataset.objects.last()
    if not latest_dataset:
        return render(request, 'model_training/no_data.html')

    # Get the dataset file path
    file_path = latest_dataset.file.path

    try:
        # Preprocess the dataset using utils.py
        X, y = preprocess_dataset(file_path)
    except ValueError as e:
        return render(request, 'model_training/no_target_column.html', {'error_message': str(e)})

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model (Random Forest)
    model = RandomForestClassifier(n_estimators=200, max_depth=10, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Replace 'f1-score' with 'f1_score' in the report keys
    for label, metrics in report.items():
        if isinstance(metrics, dict) and "f1-score" in metrics:
            metrics["f1_score"] = metrics.pop("f1-score")

    # Ensure the 'models' directory exists and save the trained model
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)  # Create the directory if it doesn't exist
    model_path = os.path.join(model_dir, "trained_model.pkl")
    joblib.dump(model, model_path)

    return render(request, 'model_training/training_results.html', {
        'dataset': latest_dataset,
        'accuracy': accuracy * 100,  # Convert to percentage
        'report': report,
        'model_path': model_path,
    })
