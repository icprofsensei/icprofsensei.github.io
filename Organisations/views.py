from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import OrganisationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Organisation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from register.models import UserProfile 
from django.contrib import messages
from django.contrib.auth import get_user_model

class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated

class OrgLanderView(BaseProtectedView, generic.ListView):
    model = Organisation
    template_name = "OrganisationMaker/Organisationlandingpage.html"
class OrgConfirmationView(generic.ListView):
    model = Organisation
    template_name = "OrganisationMaker/confirmation.html"





@login_required
def register_organisation(request):
    User = get_user_model()  # Get the user model
    if request.method == 'POST':
        form = OrganisationForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)

            # Retrieve the specified org admin username from the form
            specified_admin_username = form.cleaned_data['org_admin']

            try:
                # Fetch the user specified as the org admin
                specified_admin = User.objects.get(username=specified_admin_username)
                organisation.org_admin = specified_admin  # Set the specified user as org admin

                # Save the organisation first
                organisation.save()

                # Create or get the Group associated with the organisation
                group, created = Group.objects.get_or_create(name=organisation.name)

                # Add the specified admin to the group
                group.user_set.add(specified_admin)

                # Update the org admin's UserProfile
                user_profile_admin, created = UserProfile.objects.get_or_create(user=specified_admin)
                user_profile_admin.organisation = organisation
                user_profile_admin.save()

                # If the specified admin is not the logged-in user, add the current user to the group
                if specified_admin != request.user:
                    group.user_set.add(request.user)

                    # Update the current user's UserProfile
                    user_profile_current, created = UserProfile.objects.get_or_create(user=request.user)
                    user_profile_current.organisation = organisation
                    user_profile_current.save()

                messages.success(request, f"Organisation '{organisation.name}' created successfully!")
                return redirect('Organisations:orgconfirmer')
            except User.DoesNotExist:
                messages.error(request, f"User '{specified_admin_username}' does not exist.")
                return redirect('Organisations:orgconfirmer')

    else:
        form = OrganisationForm()

    return render(request, 'OrganisationMaker/register_organisation.html', {'form': form})
