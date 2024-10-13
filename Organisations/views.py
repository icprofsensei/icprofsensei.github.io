from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import OrganisationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Organisation
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated

class OrgLanderView(BaseProtectedView, generic.ListView):
    model = Organisation
    template_name = "OrganisationMaker/organisationlandingpage.html"
class OrgConfirmationView(generic.ListView):
    model = Organisation
    template_name = "OrganisationMaker/confirmation.html"


@login_required
def register_organisation(request):
    if request.method == 'POST':
        form = OrganisationForm(request.POST)
        if form.is_valid():
            organisation = form.save(commit=False)
            #organisation.org_admin = request.user  # Set the primary user as the logged-in user
            organisation.save()
            return redirect('Organisations:orgconfirmer')
    else:
        form = OrganisationForm()

    return render(request, 'OrganisationMaker/register_organisation.html', {'form': form})