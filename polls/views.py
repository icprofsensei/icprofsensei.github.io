from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Choice, Question, Vote
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from register.models import UserProfile
class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated
class IndexView(BaseProtectedView, generic.ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
    ]
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

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
class BreakdownView(generic.DetailView):
    model = Question
    template_name = "polls/breakdown.html"


@login_required 
def vote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if Vote.objects.filter(user=request.user, question=question).exists():
        # If the user has already voted, show a message or redirect to results
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(
            request,
            "polls/detail.html",
            {
            "question": question,
            "error_message": "You didn't select a choice.",
            },)
        else:
            Vote.objects.create(user=request.user, question=question, choice=selected_choice)
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_has_voted = Vote.objects.filter(user=request.user, question=question).exists()
    return render(request, 'polls/detail.html', {
        'question': question,
        'user_has_voted': user_has_voted,
    })

@login_required
def redo_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        # Find the user's vote for the specific question
        user_vote = Vote.objects.get(question=question, user=request.user)
        user_vote.delete()  # Remove the vote
        choice = user_vote.choice
        if choice.votes > 0:  # Ensure it doesn't go below 0
            choice.votes -= 1
            choice.save() 
    except Vote.DoesNotExist:
        # If no vote exists for this user, do nothing
        pass
    
    # After removing the vote, redirect them back to the voting page for the question
    return HttpResponseRedirect(reverse("polls:vote", args=(question.id,)))

