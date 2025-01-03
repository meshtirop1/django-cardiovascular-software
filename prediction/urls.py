from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.make_prediction, name='make_prediction'),
]
