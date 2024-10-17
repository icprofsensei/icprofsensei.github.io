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
    if request.method == 'POST':
        form = OrganisationForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)
            organisation.org_admin = request.user  # Set the logged-in user as the org admin
            organisation.save()

            # Create or get the Group associated with the organisation
            group, created = Group.objects.get_or_create(name=organisation.name)

            # Add the org admin to the group
            group.user_set.add(organisation.org_admin)

            # Update the org admin's UserProfile
            user_profile_admin, created = UserProfile.objects.get_or_create(user=organisation.org_admin)
            user_profile_admin.organisation = organisation
            user_profile_admin.save()

            # Add the current user to the group if they are not the org admin
            if request.user != organisation.org_admin:
                group.user_set.add(request.user)

                # Update the current user's UserProfile
                user_profile_current, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile_current.organisation = organisation
                user_profile_current.save()

            messages.success(request, f"Organisation '{organisation.name}' created successfully!")
            return redirect('Organisations:orgconfirmer')
    else:
        form = OrganisationForm()

    return render(request, 'OrganisationMaker/register_organisation.html', {'form': form})