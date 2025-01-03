import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render

def evaluate_model(request):
    # Load the saved model
    try:
        model = joblib.load("models/trained_model.pkl")
    except FileNotFoundError:
        return render(request, 'evaluation/no_model.html')

    # Load the latest dataset
    dataset_path = "C:/Users/mtiro/Downloads/large_disease_detection_dataset.csv"  # Path to the dataset
    try:
        data = pd.read_csv(dataset_path)
    except FileNotFoundError:
        return render(request, 'evaluation/no_test_data.html')

    # Ensure the dataset has the target column
    if "Disease" not in data.columns:
        return render(request, 'evaluation/no_target_column.html')

    # Split into features and target
    X_test = data.drop(columns=["Disease"])
    y_test = data["Disease"]

    # Generate predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Generate a confusion matrix heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    confusion_matrix_image = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'evaluation/evaluation_results.html', {
        'accuracy': accuracy,
        'report': report,
        'confusion_matrix_image': confusion_matrix_image,
    })
