from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

User = get_user_model()


class BaseMeta:
    exclude = '__all__'
    fields = ('username', 'first_name', 'last_name', 'email')


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta(BaseMeta):
        model = User

