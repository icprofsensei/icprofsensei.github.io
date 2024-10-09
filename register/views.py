from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
# Create your views here.



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("/polls/")  # Redirect to login page after successful registration
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})