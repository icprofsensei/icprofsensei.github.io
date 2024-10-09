from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Renders the home.html template
def purpose(request):
    return render(request, 'purpose.html')