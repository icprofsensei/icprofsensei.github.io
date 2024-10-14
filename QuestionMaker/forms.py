from django import forms
from polls.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', 'organisation']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'question_text': 'Question Text',
            'pub_date': 'Publish Date',
            'organisation' : 'Organisation-access ONLY (optional)'
        }