from django.db.models import Model, DecimalField, PositiveIntegerField, DateTimeField
from django.db import models
from training_plans.models import ExerciseSet


class ExerciseSetPerformance(Model):
    weight = DecimalField(max_digits=4, decimal_places=1)
    repetitions_done = PositiveIntegerField()
    estimated_max = DecimalField(max_digits=4, decimal_places=1)
    bodyweight = DecimalField(max_digits=4, decimal_places=1)
    date = DateTimeField(auto_now_add=True)
    exercise_set = models.ForeignKey(
        ExerciseSet, on_delete=models.CASCADE, related_name="performances"
    )
