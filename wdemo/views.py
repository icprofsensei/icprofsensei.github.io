from django.shortcuts import get_object_or_404, render
from Organisations.models import UserProfile
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')  # Renders the home.html template
def purpose(request):
    return render(request, 'purpose.html')
@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    organisation = user_profile.organisation
    return render(request, 'profile.html', {'organisation': organisation})