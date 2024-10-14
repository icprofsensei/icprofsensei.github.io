from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from Organisations.models import Organisation
# Create your models here. Imagine each class as a unique table 

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    organisation = models.ForeignKey(Organisation, on_delete=models.SET_NULL, null=True, blank=True)  # Optional: Only for a specific organization
    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete= models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)
    manifesto_text = models.TextField(null=True, blank=True)  # Optional field for manifestos
    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign key because it links to the in-built user ids in SQL
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Foreign key because it links to the question ids 
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE) # Foreign key because it links to the choices

    class Meta:
        unique_together = ('user', 'question') # 1 user for every 1 question
    def __str__(self):
        return f"{self.user.username} voted on {self.question}"
    # We do the above to define how the model would be represented as a string. 

