from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

User = get_user_model()


class BaseMeta:
    model = User
    exclude = '__all__'
    fields = ('username', 'first_name', 'last_name', 'email')


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta(BaseMeta):
        pass


class UserEditForm(auth_forms.UserChangeForm):
    class Meta(BaseMeta):
        fields = ('first_name', 'last_name', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password')
