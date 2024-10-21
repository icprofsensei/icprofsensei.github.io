from django import forms
from .models import QuestionaireQ, AnswerOption, UserAnswer

class QuestionnaireForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile')
        super(QuestionnaireForm, self).__init__(*args, **kwargs)

        # Dynamically create form fields for each question
        for question in QuestionaireQ.objects.all():
            answer_choices = AnswerOption.objects.filter(question=question)
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                queryset=answer_choices,
                widget=forms.RadioSelect,
                label=question.text,
                required=True
            )

    def save(self, user_profile):
        # Save the answers
        for field_name, selected_option in self.cleaned_data.items():
            if field_name.startswith('question_'):
                question_id = field_name.split('_')[1]
                question = QuestionaireQ.objects.get(id=question_id)
                UserAnswer.objects.create(
                    user_profile=user_profile,
                    question=question,
                    selected_option=selected_option
                )
