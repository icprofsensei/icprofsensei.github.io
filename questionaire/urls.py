from django.urls import path
from .views import QuestionnaireView, ThankView

app_name = 'questionaire'

urlpatterns = [
    path('', QuestionnaireView.as_view(), name='questionaire_form'),
    path('thank-you/', ThankView.as_view(), name='thank_you'),]