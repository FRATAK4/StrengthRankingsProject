from django.db import models

from training_plans.models import ExerciseSet


class ExerciseSetPerformance(models.Model):
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    repetitions_done = models.IntegerField()
    estimated_max = models.DecimalField(max_digits=4, decimal_places=1)
    bodyweight = models.DecimalField(max_digits=4, decimal_places=1)
    date = models.DateTimeField()
    exercise_set = models.ForeignKey(ExerciseSet, on_delete=models.CASCADE, related_name='performances')