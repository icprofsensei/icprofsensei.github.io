from django.contrib import admin
from .models import QuestionaireQ, AnswerOption, UserAnswer
# Register your models here.
admin.site.register(QuestionaireQ)
admin.site.register(AnswerOption)
admin.site.register(UserAnswer)