from django.contrib import admin

from .models import TrainingPlan, Workout, ExerciseSet

admin.site.register(TrainingPlan)
admin.site.register(Workout)
admin.site.register(ExerciseSet)
