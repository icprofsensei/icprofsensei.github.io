from django.shortcuts import get_object_or_404, render, redirect
from register.models import UserProfile
from django.contrib.auth.decorators import login_required
from datetime import date


def home(request):
    return render(request, 'home.html')  # Renders the home.html template
def purpose(request):
    return render(request, 'purpose.html')


@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.date_of_birth:
                today = date.today()
                age = today.year - user_profile.date_of_birth.year - ((today.month, today.day) < (user_profile.date_of_birth.month, user_profile.date_of_birth.day))
    else:
                age = None 
    organisation = user_profile.organisation
    print(f'User: {request.user.username}, Organisation: {organisation}, Age: {age}')
    return render(request, 'profile.html', {'user':user_profile, 'organisation': organisation, 'age':age})