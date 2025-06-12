from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from exercises.models import Exercise


class TrainingPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="training_plans"
    )


class Workout(models.Model):
    class Days(models.TextChoices):
        MONDAY = "monday"
        TUESDAY = "tuesday"
        WEDNESDAY = "wednesday"
        THURSDAY = "thursday"
        FRIDAY = "friday"
        SATURDAY = "saturday"
        SUNDAY = "sunday"

    name = models.CharField(max_length=50)
    description = models.TextField()
    day = models.CharField(max_length=30, choices=Days.choices)
    training_plan = models.ForeignKey(
        TrainingPlan, on_delete=models.CASCADE, related_name="workouts"
    )


class ExerciseSet(models.Model):
    set_index = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(50),
        ]
    )
    repetitions = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ]
    )
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="exercise_sets_using"
    )
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="exercise_sets"
    )


class TrainingPlanUsage(models.Model):
    is_active = models.BooleanField(default=False)
    training_plan = models.ForeignKey(
        TrainingPlan, on_delete=models.CASCADE, related_name="user_usages"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="training_usages"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("training_plan", "user"),)


class TrainingPlanRating(models.Model):
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    training_plan = models.ForeignKey(
        TrainingPlan, on_delete=models.CASCADE, related_name="user_ratings"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="training_plan_ratings"
    )

    class Meta:
        unique_together = (("training_plan", "user"),)
