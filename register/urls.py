from django.urls import path
from . import views

app_name = 'register'  # Namespace for your register app

urlpatterns = [
    path('', views.register_step_1, name='register_step_1'),
    path('extra-info/', views.register_step_2, name='register_step_2'),
]