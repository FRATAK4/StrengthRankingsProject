from django.db.models import Model, DecimalField, PositiveIntegerField, DateTimeField
from decimal import Decimal
from datetime import datetime
from django.db import models
from training_plans.models import ExerciseSet


class ExerciseSetPerformance(Model):
    weight: DecimalField = DecimalField(max_digits=4, decimal_places=1)
    repetitions_done: PositiveIntegerField = PositiveIntegerField()
    estimated_max: DecimalField = DecimalField(max_digits=4, decimal_places=1)
    bodyweight: DecimalField = DecimalField(
        max_digits=4, decimal_places=1
    )  # TODO inna nazwa
    date: DateTimeField = DateTimeField(auto_now_add=True)
    exercise_set: models.ForeignKey = models.ForeignKey(
        ExerciseSet, on_delete=models.CASCADE, related_name="performances"
    )
