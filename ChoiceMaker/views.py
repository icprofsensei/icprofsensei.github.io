from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Question
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseProtectedView(LoginRequiredMixin):
    login_url = '/login/'  # Redirect to this URL if not authenticated

class IndexChoiceView(generic.ListView):
    template_name = "ChoiceMaker/openpolls.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
    ]

class ChoiceMakerView(BaseProtectedView, generic.DetailView):
    model = Question
    template_name = "ChoiceMaker/partymaker.html"

def add_choice(request, question_id):
    # Fetch the question based on the provided question_id in the URL
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        # Get the input data from the form (field name is 'partyname')
        party_name = request.POST.get('partyname')
        manifesto = request.POST.get('manifesto')
        if not party_name:
            # If no party name is provided, show an error
            return render(
                request, 
                'ChoiceMaker/partymaker.html',  # Replace with your actual template name
                {
                    'question': question, 
                    'error_message': 'You must provide a party name.'
                }
            )

        # Create a new Choice object and associate it with the question
        choice = Choice(question=question, choice_text=party_name, manifesto_text = manifesto, votes=0)
        choice.save()

        # Redirect to the same page or another page, e.g., the question detail view
        return render(request, 'ChoiceMaker/confirmation.html', {'question': question})

    # If the request method is GET, render the form
    return render(request, 'ChoiceMaker/confirmation.html', {'question': question})