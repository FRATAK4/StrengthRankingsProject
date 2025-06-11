from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from exercises.models import Exercise


class TrainingPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    is_active = models.BooleanField()
    is_public = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_plans')

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
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='workouts')

class ExerciseSet(models.Model):
    set_index = models.IntegerField()
    repetitions = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_sets_using')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercise_sets')

class TrainingPlanUsage(models.Model):
    is_active = models.BooleanField()
    get_at = models.DateField(default=datetime.now)
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='user_usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_usages')

    class Meta:
        unique_together = (('training_plan', 'user'),)

class TrainingPlanRating(models.Model):
    rating = models.IntegerField()
    comment = models.CharField(max_length=2000)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField()
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE, related_name='user_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_plan_ratings')

    class Meta:
        unique_together = (('training_plan', 'user'),)