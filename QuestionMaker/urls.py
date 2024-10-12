from django.urls import path

from . import views

app_name = "QuestionMaker"
urlpatterns = [
    path("", views.QuestionLanderView.as_view(), name="questionlander"),
    path("newquestion/", views.add_question, name = "questionmaker"),
    path("newquestion/confirmed/", views.QuestionConfirmationView.as_view(), name = "questionconfirmer"), # this is a class-based view so needs the .as_view() to convert it to a view. 
]