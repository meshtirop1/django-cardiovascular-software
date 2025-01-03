from django.urls import path, include
from .views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('data/', include('data_management.urls')),
    path('visualization/', include('visualization.urls')),
    path('training/', include('model_training.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('prediction/', include('prediction.urls')),
    path('user_management/', include('user_management.urls')),
]
