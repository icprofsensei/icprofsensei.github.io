from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Organisations.models import Organisation
from .models import UserProfile
class RegisterForm(UserCreationForm):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all(), required=False)
    email = forms.EmailField()
    organisation_password = forms.CharField(widget=forms.PasswordInput, required=False)  # Make it optional
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "organisation", "organisation_password"]

class ExtraInfoForm(forms.Form):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs = {'type': 'date'}), required = True)
    ethnicity = forms.ChoiceField(choices=UserProfile.ETHNICITY_CHOICES, required=True)  # Add ethnicity dropdown
class CustomAuthenticationForm(AuthenticationForm):
    organisation = forms.ModelChoiceField(queryset=Organisation.objects.all(), required=False, empty_label="Select your organisation")