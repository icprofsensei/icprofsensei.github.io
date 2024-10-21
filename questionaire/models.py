from django.db import models
from register.models import UserProfile  # Assuming your UserProfile is in MyOrg app

class QuestionaireQ(models.Model):
    text = models.CharField(max_length=255)  # The question text
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(QuestionaireQ, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)  # The possible answer text

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(QuestionaireQ, on_delete=models.CASCADE, related_name='user_answers')
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, related_name='user_answers')
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} answered '{self.selected_option.text}' for '{self.question.text}'"
