from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from Organisations.forms import OrganisationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from Organisations.models import Organisation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from register.models import UserProfile 

class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated

class HomeOrg(BaseProtectedView, generic.ListView):
    model = Organisation
    template_name = "MyOrg/homeorg_landingpage.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        context['organisation'] = user_profile.organisation  # Pass organisation to context
        
        # Get questions related to the organisation
        context['orgquestions'] = self.model.objects.filter(id=user_profile.organisation.id).first().question_set.all() if user_profile.organisation else []  
        
        return context
