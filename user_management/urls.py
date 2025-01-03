from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Import views from user_management app to use in urlpatterns

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='user_management/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),




]
