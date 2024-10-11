from django.urls import path

from . import views

app_name = "ChoiceMaker"
urlpatterns = [
    path("", views.IndexChoiceView.as_view(), name="openpolls"),
    path("<int:pk>/", views.ChoiceMakerView.as_view(), name="makechoice"),
    path("<int:question_id>/add_choice/", views.add_choice, name="add_choice"),
]