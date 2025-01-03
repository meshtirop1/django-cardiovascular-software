from django.urls import path
from . import views

urlpatterns = [
    path('evaluate/', views.evaluate_model, name='evaluate_model'),
]
