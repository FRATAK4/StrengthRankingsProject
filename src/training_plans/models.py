from django.db import models
from django.contrib.auth.models import User

class TrainingPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
