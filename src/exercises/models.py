from django.db import models

class Exercise(models.Model):
    class Exercises(models.TextChoices):
        BENCH_PRESS = 'bench_press'
        DEADLIFT = 'deadlift'
        SQUAT = 'squat'

    name = models.CharField(max_length=50, choices=Exercises.choices)
