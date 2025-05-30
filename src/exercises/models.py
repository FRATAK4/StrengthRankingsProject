from django.db import models


class Exercise(models.Model):
    class Exercises(models.TextChoices):
        BENCH_PRESS = 'bench_press'
        DEADLIFT = 'deadlift'
        SQUAT = 'squat'

    name = models.CharField(max_length=50, choices=Exercises.choices)
    description = models.CharField(max_length=2000)

class MuscleActivation(models.Model):
    class Muscles(models.TextChoices):
        CHEST = 'chest'
        TRICEPS = 'triceps'
        SHOULDERS = 'shoulders'
        QUADRICEPS = 'quadriceps'
        HAMSTRING = 'hamstring'

    muscle = models.CharField(max_length=50, choices=Muscles.choices)
    activation_level = models.IntegerField()
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
