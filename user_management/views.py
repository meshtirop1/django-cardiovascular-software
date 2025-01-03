from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json


from django.contrib.auth.decorators import login_required
from .models import PredictionHistory



@login_required
def dashboard(request):
    predictions = PredictionHistory.objects.filter(user=request.user).order_by('-created_at')
    for prediction in predictions:
        prediction.input_data = json.loads(prediction.input_data)  # Deserialize input data
        prediction.confidence_scores = json.loads(prediction.confidence_scores)  # Deserialize scores
    return render(request, 'user_management/dashboard.html', {'predictions': predictions})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('make_prediction')
    else:
        form = UserCreationForm()
    return render(request, 'user_management/signup.html', {'form': form})
