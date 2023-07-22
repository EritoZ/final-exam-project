from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from apps.accounts import forms

User = get_user_model()


# Create your views here.

class RegisterView(generic.CreateView):
    template_name = 'account/register-page.html'
    model = User
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('index')


class LoginView(auth_views.LoginView):
    template_name = 'account/login-page.html'


class LogoutView(auth_views.LogoutView):
    pass
