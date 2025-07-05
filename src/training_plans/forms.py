from django import forms
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseSet
from django.forms import inlineformset_factory


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["name", "description", "is_active", "is_public"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ["name", "description", "day"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "day": forms.Select(attrs={"class": "form-control"}),
        }


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ["exercise"]
        widgets = {
            "exercise": forms.Select(attrs={"class": "form-select"}),
        }


class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ["set_number", "repetitions"]
        widgets = {
            "set_number": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "repetitions": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


WorkoutFormSet = inlineformset_factory(
    TrainingPlan,
    Workout,
    form=WorkoutForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)

WorkoutExerciseFormSet = inlineformset_factory(
    Workout,
    WorkoutExercise,
    form=WorkoutExerciseForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)

ExerciseSetFormSet = inlineformset_factory(
    WorkoutExercise,
    ExerciseSet,
    form=ExerciseSetForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)
