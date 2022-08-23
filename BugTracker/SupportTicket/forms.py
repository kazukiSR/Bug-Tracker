from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=256, help_text='Required. Add a valid email address.')

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean(self):
        if self.is_valid():
            email = self.clean_email()
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")
