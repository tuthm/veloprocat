from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label="Логин", max_length=60)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя и фамилия", max_length=50)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Этот email уже занят")
        return email
