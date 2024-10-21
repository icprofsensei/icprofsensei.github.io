from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .forms import QuestionForm
from polls.models import Choice, Question
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from register.models import UserProfile
class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated

class QuestionLanderView(BaseProtectedView, generic.ListView):
    context_object_name = "question_list"
    model = Question
    template_name = "QuestionMaker/questionlandingpage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user's profile and associated organisation
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        
        # Pass organisation to context
        context['organisation'] = user_profile.organisation  
        
        # Check if the organisation exists and fetch related questions
        if user_profile.organisation:
            # Assuming you have a ForeignKey to Organisation in the Question model
            organisation_questions = self.model.objects.filter(organisation=user_profile.organisation)
            context['orgquestions'] = organisation_questions
        else:
            context['orgquestions'] = []
        
        return context
class QuestionConfirmationView(generic.ListView):
    model = Question
    template_name = "QuestionMaker/confirmation.html"

def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the new question to the database
            question = form.save(commit=False)
            question.pub_date = timezone.now()  # Set the current time as the publish date
            question.save()
            return redirect('QuestionMaker:questionconfirmer')  # Redirect to the question confirmation page
    else:
        form = QuestionForm()  # Display an empty form if the request is GET

    return render(request, 'QuestionMaker/questionmaker.html', {'form': form})