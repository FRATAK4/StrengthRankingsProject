from django import forms
from .models import TrainingPlan, Workout, ExerciseSet


class TrainingPlanCreateForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["name", "description", "is_active", "is_public"]


class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["name", "description", "day"]


class ExerciseSetCreateForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ["set_index", "repetitions", "exercise"]
