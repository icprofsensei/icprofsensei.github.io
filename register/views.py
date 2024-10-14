from django.shortcuts import render, redirect
from .forms import RegisterForm, CustomAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from Organisations.models import UserProfile, Organisation

# Registration view for new users
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Check if UserProfile already exists or create a new one
            UserProfile.objects.get_or_create(user=user)
            
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("/")  # Redirect to home or another page
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

# Custom login view for users
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
                login(request, user)
                messages.success(request, f"Welcome {user.username}!")
                
                # Store the selected organisation in the session if available
                if organisation:
                    request.session['organisation_id'] = organisation.id
                else:
                    request.session['organisation_id'] = None  # Clear if no organisation selected

                return redirect('/')  # Redirect after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})
