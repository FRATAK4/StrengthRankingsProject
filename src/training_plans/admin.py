from django.contrib import admin

from .models import TrainingPlan, Workout, ExerciseSet, TrainingPlanUsage, TrainingPlanRating

admin.site.register(TrainingPlan)
admin.site.register(Workout)
admin.site.register(ExerciseSet)
admin.site.register(TrainingPlanUsage)
admin.site.register(TrainingPlanRating)
