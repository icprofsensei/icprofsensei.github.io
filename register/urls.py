from django.urls import path
from . import views

app_name = 'register'  # Namespace for your register app

urlpatterns = [
    path('', views.register, name='register'),
]