from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя."""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Повторите пароль"})
