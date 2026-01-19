
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'}), min_length=8)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirme a senha'}), min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'age']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está em uso.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError('As senhas não coincidem.')
            validate_password(password1)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
from django import forms

from .models import (
    User,
    reminder,
    Task
)


class userForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
            "email"
        ]


# Formulário para tarefas
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "scheduled_time"]
