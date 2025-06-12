from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Exercise(models.Model):
    class Exercises(models.TextChoices):
        BENCH_PRESS = "bench_press"
        DEADLIFT = "deadlift"
        SQUAT = "squat"

    name = models.CharField(max_length=50, choices=Exercises.choices)
    description = models.TextField()


class MuscleActivation(models.Model):
    class Muscles(models.TextChoices):
        CHEST = "chest"
        TRICEPS = "triceps"
        SHOULDERS = "shoulders"
        QUADRICEPS = "quadriceps"
        HAMSTRING = "hamstring"

    muscle = models.CharField(max_length=50, choices=Muscles.choices)
    activation_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="muscles_activation"
    )
