from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from Organisations.models import Organisation
from django import forms
from django.views import generic,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from register.models import UserProfile 
from django.contrib import messages
from django.views.generic.edit import UpdateView
from datetime import date
from django.utils.decorators import method_decorator

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


class ProfileView(BaseProtectedView, generic.ListView):
    model = Organisation
    template_name = 'MyOrg/profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        organisation = user_profile.organisation

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        organisation = user_profile.organisation
        ethnicity = user_profile.ethnicity
        if user_profile.date_of_birth:
            today = date.today()
            age = today.year - user_profile.date_of_birth.year - ((today.month, today.day) < (user_profile.date_of_birth.month, user_profile.date_of_birth.day))
        else:
            age = None 
        context = {
            'organisation': organisation,
            'age': age,
            'ethnicity':ethnicity
        } 
        
        return context

class OrgAdmin(BaseProtectedView, generic.ListView):
    model = Organisation
    template_name = "MyOrg/adminpage.html"

    def dispatch(self, request, *args, **kwargs):
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        organisation = user_profile.organisation
        
        # Check if the user is the organisation admin
        if organisation and user_profile.user != organisation.org_admin:
            messages.error(request, "You do not have permission to access this page as you are not the organisation admin")
            return redirect('/')  # Redirect to home or another appropriate page

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        organisation = user_profile.organisation
        organisation_group = Group.objects.get(name=organisation.name)
        users_in_group = organisation_group.user_set.all()
        context['organisation'] = organisation  # Pass organisation to context
        context['users_in_group'] = users_in_group
        # Get questions related to the organisation
        context['orgquestions'] = organisation.question_set.all() if organisation else []  
        
        return context

class RemoveUserForm(forms.Form):
    user_to_remove = forms.ModelChoiceField(
        queryset=UserProfile.objects.none(),  # We'll populate this in the view
        empty_label="Select a user",
        label="User to remove"
    )

class EditUserView(BaseProtectedView, View):
    template_name = 'MyOrg/editorg_page.html'

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        organisation = user_profile.organisation
        
        # Get all users in the organization
        users_in_org = UserProfile.objects.filter(organisation=organisation)

        # Create the form and populate the dropdown
        form = RemoveUserForm()
        form.fields['user_to_remove'].queryset = users_in_org

        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        organisation = user_profile.organisation
        users_in_org = UserProfile.objects.filter(organisation=organisation)

        form = RemoveUserForm(request.POST)
        form.fields['user_to_remove'].queryset = users_in_org

        if form.is_valid():
            user_to_remove = form.cleaned_data['user_to_remove']
            if user_to_remove == user_profile:
                # Check if this user is the only one in the organisation
                if users_in_org.count() == 1:
                    # If they are the only member, delete the organisation's group
                    try:
                        organisation_group = Group.objects.get(name=organisation.name)
                        organisation_group.delete()  # Delete the group
                        messages.success(request, "The organisation's group has been deleted as you were the last member.")
                    except Group.DoesNotExist:
                        messages.warning(request, "No group found for this organisation to delete.")
                    
                    # Also remove the organisation itself if that's the intended behavior
                    organisation.delete()
                    messages.success(request, "Organisation has been deleted as there were no members left.")
                    
                    # Log the user out or redirect to a fallback page, as the organisation no longer exists
                    return redirect('/')  # Or a suitable fallback page
                    
                else:
                    # Prevent a user from removing themselves if other members are still in the organisation
                    messages.error(request, "You cannot remove yourself while there are other members in the organisation.")
                    return redirect('MyOrg:orgadmin')  # Redirect back to the admin page

            else:
                # Remove the user from the organisation
                user_to_remove.organisation = None
                user_to_remove.save()
                messages.success(request, f"User {user_to_remove.user.username} has been removed from the organisation.")
                
            return redirect('MyOrg:orgadmin')

        return render(request, self.template_name, {'form': form})