from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('create', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
]