from django.db import models
from django.contrib.auth.models import User

class TrainingPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    is_active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Workout(models.Model):
    class Days(models.TextChoices):
        MONDAY = 'monday'
        TUESDAY = 'tuesday'
        WEDNESDAY = 'wednesday'
        THURSDAY = 'thursday'
        FRIDAY = 'friday'
        SATURDAY = 'saturday'
        SUNDAY = 'sunday'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    day = models.CharField(max_length=30, choices=Days.choices)
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)