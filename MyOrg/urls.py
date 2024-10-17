from django.urls import path

from . import views

app_name = "MyOrg"
urlpatterns = [
    path("", views.HomeOrg.as_view(), name="homeorglander"),
]