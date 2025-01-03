from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Dataset
import pandas as pd
from .forms import DatasetForm
from .utils import preprocess_dataset  # Import preprocessing function


def upload_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save()  # Save the dataset instance
            file_path = dataset.file.path  # Get the file path

            # Preprocess the dataset to ensure validity
            try:
                data = preprocess_dataset(file_path)  # Returns preprocessed data
                # Use the original dataset to call `.head()` for display
                original_data = pd.read_csv(file_path)
            except ValueError as e:
                return render(request, 'data_management/upload_error.html', {'error_message': str(e)})

            # Display the first rows of the original dataset
            preview = original_data.head()

            return render(request, 'data_management/upload_success.html', {
                'dataset': dataset,
                'preview': preview.to_html(classes='table table-bordered'),
            })
    else:
        form = DatasetForm()

    return render(request, 'data_management/upload.html', {'form': form})
