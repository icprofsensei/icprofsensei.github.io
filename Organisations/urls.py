from django.urls import path

from . import views

app_name = "Organisations"
urlpatterns = [
    path("", views.OrgLanderView.as_view(), name="organisationlander"),
    path("neworg/", views.register_organisation, name = "organisationmaker"),
    path("neworg/confirmed/", views.OrgConfirmationView.as_view(), name = "orgconfirmer"), # this is a class-based view so needs the .as_view() to convert it to a view. 
]