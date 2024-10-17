from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from Organisations.models import Organisation
from .models import UserProfile

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Fetch the selected organisation from the cleaned data
            organisation = form.cleaned_data.get('organisation')

            # Create the user instance
            user = form.save()

            # Check if an organisation is selected
            if organisation:
                # Ensure the user enters the correct password for the organisation
                organisation_password = form.cleaned_data.get('organisation_password')
                if organisation.check_password(organisation_password):
                    # Create the UserProfile associated with the user
                    user_profile = UserProfile.objects.create(user=user, organisation=organisation)
                    user_profile.save()
                else:
                    messages.error(request, "Incorrect organisation password.")
                    return redirect("register")  # Redirect back to registration page
            else:
                # No organisation selected, create the UserProfile without an organisation
                UserProfile.objects.create(user=user, organisation=None)

            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")

            # Store the selected organisation in the session if available
            request.session['organisation_id'] = organisation.id if organisation else None
            
            return redirect("/")  # Redirect to home or another page
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})




def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            organisation = form.cleaned_data.get('organisation')

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check organisation password if an organisation is selected
                if organisation:
                    organisation_password = form.cleaned_data.get('organisation_password')
                    if organisation.check_password(organisation_password):
                        login(request, user)
                        messages.success(request, f"Welcome {user.username}!")
                        request.session['organisation_id'] = organisation.id
                        return redirect('/')  # Redirect after login
                    else:
                        messages.error(request, "Incorrect organisation password.")
                else:
                    login(request, user)
                    messages.success(request, f"Welcome {user.username}!")
                    request.session['organisation_id'] = None
                    return redirect('/')  # Redirect after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})
