import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from django.shortcuts import render
from data_management.models import Dataset

def visualize_data(request):
    # Load the latest uploaded dataset
    latest_dataset = Dataset.objects.last()
    if not latest_dataset:
        return render(request, 'visualization/no_data.html')

    # Load the dataset into a DataFrame
    file_path = latest_dataset.file.path
    data = pd.read_csv(file_path)

    # Generate visualizations
    graph_images = []
    numeric_columns = data.select_dtypes(include=['number']).columns

    if len(numeric_columns) == 0:
        return render(request, 'visualization/no_numeric_data.html', {'dataset': latest_dataset})

    # Generate histograms for up to 2 numeric columns
    for column in numeric_columns[:2]:
        plt.figure(figsize=(8, 6))
        data[column].hist(bins=20, color='skyblue', edgecolor='black')
        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph_images.append(base64.b64encode(image_png).decode('utf-8'))

    # Generate a correlation heatmap if there are multiple numeric columns
    if len(numeric_columns) > 1:
        plt.figure(figsize=(10, 8))
        correlation_matrix = data[numeric_columns].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph_images.append(base64.b64encode(image_png).decode('utf-8'))

    return render(request, 'visualization/visualize.html', {
        'dataset': latest_dataset,
        'graphs': graph_images,
    })
