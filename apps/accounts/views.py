from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth import models as auth_models
from django.urls import reverse_lazy, reverse
from django.views import generic

from apps.accounts import forms

User = get_user_model()


# Create your views here.

class BaseProfileView:
    model = User


class RegisterView(generic.CreateView):
    template_name = 'account/register-page.html'
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        result = super().form_valid(form)

        auth_models.Group.objects.get(name='regular_user_group').user_set.add(self.object)

        return result


class LoginView(auth_views.LoginView):
    template_name = 'account/login-page.html'


class LogoutView(auth_views.LogoutView):
    pass


class ProfileDetailsView(BaseProfileView, generic.DetailView):
    template_name = 'account/details-profile-page.html'


class ProfileEditView(BaseProfileView, generic.UpdateView):
    template_name = 'account/edit-profile-page.html'
    form_class = forms.UserEditForm

    def get_success_url(self):
        return reverse('profile details', kwargs={'slug': self.object.slug})
