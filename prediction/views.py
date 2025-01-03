import joblib
import numpy as np
import json  # For serializing and deserializing JSON data
from django.shortcuts import render
from .forms import PredictionForm
from user_management.models import PredictionHistory

def make_prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            user_data = np.array([
                form.cleaned_data['age'],
                form.cleaned_data['cholesterol'],
                form.cleaned_data['blood_pressure'],
                form.cleaned_data['smoking'],
                form.cleaned_data['diabetes']
            ]).reshape(1, -1)

            try:
                model = joblib.load("models/trained_model.pkl")
            except FileNotFoundError:
                return render(request, 'prediction/no_model.html')

            prediction = model.predict(user_data)[0]
            prediction_prob = model.predict_proba(user_data)[0]

            # Save to PredictionHistory with serialized data
            if request.user.is_authenticated:
                PredictionHistory.objects.create(
                    user=request.user,
                    input_data=json.dumps(form.cleaned_data),  # Serialize input data to JSON string
                    prediction=prediction,
                    confidence_scores=json.dumps(prediction_prob.tolist()),  # Serialize scores to JSON string
                )

            return render(request, 'prediction/results.html', {
                'form': form,
                'prediction': prediction,
                'prediction_prob': prediction_prob,
            })
    else:
        form = PredictionForm()

    return render(request, 'prediction/predict.html', {'form': form})
