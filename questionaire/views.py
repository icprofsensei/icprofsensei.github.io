from django.shortcuts import render, redirect
from .forms import QuestionnaireForm
from django.contrib.auth.mixins import LoginRequiredMixin
from register.models import UserProfile
from django.urls import reverse
from django.views.generic import FormView
from django.views import generic
from .models import QuestionaireQ, UserAnswer
class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated


class QuestionnaireView(BaseProtectedView, FormView):
    template_name = 'questionaire/questionaire_form.html'
    form_class = QuestionnaireForm

    def get_form_kwargs(self):
        """
        Pass the user's profile to the form so that the form can generate the questions
        and answer options specific to the user.
        """
        kwargs = super().get_form_kwargs()
        user_profile = UserProfile.objects.get(user=self.request.user)  # Get the user profile
        kwargs['user_profile'] = user_profile  # Pass user profile to the form
        return kwargs

    def form_valid(self, form):
        """
        If the form is valid, save the user's answers and associate them with the UserProfile.
        """
        user_profile = UserProfile.objects.get(user=self.request.user)
        for field_name, selected_option in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = field_name.split('_')[1]
                question = QuestionaireQ.objects.get(id=question_id)
                
                # Update or create the user's answer
                UserAnswer.objects.update_or_create(
                    user_profile=user_profile,
                    question=question,
                    defaults={'selected_option': selected_option}
                )
        
        # Use `reverse()` to generate the success URL dynamically
        return redirect(reverse('questionaire:thank_you'))
    
class ThankView(BaseProtectedView, generic.ListView):
    model = QuestionaireQ
    template_name = 'questionaire/thanks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Retrieve the user's profile
        user_profile = UserProfile.objects.get(user=self.request.user)
        
        # Fetch all answers given by the user
        user_answers = UserAnswer.objects.filter(user_profile=user_profile)

        # Pass the user's answers to the context
        context['user_answers'] = user_answers
        
        return context