from datetime import datetime

from django.db import models

from training_plans.models import ExerciseSet


class ExerciseSetPerformance(models.Model):
    weight = models.DecimalField(decimal_places=1)
    repetitions_done = models.IntegerField()
    estimated_max = models.DecimalField(decimal_places=1)
    bodyweight = models.DecimalField(decimal_places=1)
    date = models.DateTimeField(default=datetime.now())
    exercise_set = models.ForeignKey(ExerciseSet, on_delete=models.CASCADE)