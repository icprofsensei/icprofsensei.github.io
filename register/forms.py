from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Organisations.models import Organisation, UserProfile
class RegisterForm(UserCreationForm):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all(), required=False)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "organisation"]
class CustomAuthenticationForm(AuthenticationForm):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all(), required=False, empty_label="Select your organisation")