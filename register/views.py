from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, CustomAuthenticationForm, ExtraInfoForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from Organisations.models import Organisation
from .models import UserProfile
from django.contrib.auth.models import User
def register_step_1(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Store form data in the session
            request.session['registration_data'] = form.cleaned_data
            return redirect('register:register_step_2')  # Redirect to step 2 for date_of_birth
    else:
        form = RegisterForm()
    
    return render(request, 'register/register.html', {'form': form})
    
def register_step_2(request):
    if request.method == "POST":
        form = ExtraInfoForm(request.POST)
        if form.is_valid():
            registration_data = request.session.get('registration_data')
            if not registration_data:
                return redirect('register:register_step_1')
            # Fetch the selected organisation from the cleaned data
            organisation = registration_data['organisation']
            dob = form.cleaned_data.get('date_of_birth')
            ethnicity = form.cleaned_data.get('ethnicity')
            # Create the user instance
            if User.objects.filter(username=registration_data['username']).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return redirect('register:register_step_1')  # Redirect back to registration step 1
            user = User.objects.create_user(
                username=registration_data['username'],
                email=registration_data['email'],
                password=registration_data['password1']
            )

            # Check if an organisation is selected
            if organisation:
                # Ensure the user enters the correct password for the organisation
                organisation_password = registration_data['organisation_password']
                if organisation.check_password(organisation_password):
                    # Create the UserProfile associated with the user
                    user_profile = UserProfile.objects.create(user=user, organisation=organisation, date_of_birth = dob, ethnicity=ethnicity)
                    user_profile.save()
                else:
                    messages.error(request, "Incorrect organisation password.")
                    return redirect("register:register_step_1")  # Redirect back to registration page
            else:
                # No organisation selected, create the UserProfile without an organisation
                UserProfile.objects.create(user=user, organisation=None, date_of_birth = dob, ethnicity=ethnicity)

            # Log the user in
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")

            # Store the selected organisation in the session if available
            request.session['organisation_id'] = organisation.id if organisation else None
            del request.session['registration_data']
            return redirect("/")  # Redirect to home or another page
    else:
        form = ExtraInfoForm()

    return render(request, "register/register_extrainfo.html", {"form": form})

def custom_login(request):
    #Clear previous messages

    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            organisation = form.cleaned_data.get('organisation')

            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Fetch the user's profile to check organisation membership
                try:
                    user_profile = UserProfile.objects.get(user=user)
                except UserProfile.DoesNotExist:
                    messages.error(request, "User profile not found.")
                    return redirect('login')  # Redirect to login page

                # If an organisation is selected, check if the user is part of it
                if organisation:
                    # Check if the user is part of the organisation
                    if user_profile.organisation != organisation:
                        messages.error(request, "You are not part of this organisation.")
                        return redirect('login')  # Redirect to login page

                # No organisation or valid organisation, proceed with normal login
                request.session['organisation_id'] = organisation.id if organisation else None
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                
                return redirect('/')  # Redirect after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
