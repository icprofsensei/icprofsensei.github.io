from django import forms
from .models import Organisation

class OrganisationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)  # Make password required

    class Meta:
        model = Organisation
        fields = ['name', 'org_admin', 'password']  # Add other fields if necessary