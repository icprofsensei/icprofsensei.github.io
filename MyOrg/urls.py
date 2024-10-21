from django.urls import path

from . import views

app_name = "MyOrg"
urlpatterns = [
    path("", views.HomeOrg.as_view(), name="homeorglander"),
    path("profile/", views.ProfileView.as_view(), name = "profile"),
    path("admin_access_only", views.OrgAdmin.as_view(), name="orgadmin"),
    path("admin_access_only/edit/", views.EditUserView.as_view(), name = "editusers"),
]