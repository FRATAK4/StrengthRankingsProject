from django.forms.models import ModelForm, inlineformset_factory
from django import forms
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseSet


class TrainingPlanForm(ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Push Pull Legs, Full Body Workout",
                    "maxlength": "50",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe your training plan goals, target muscles, frequency, etc.",
                }
            ),
        }


class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = ["name", "description"]


class WorkoutExerciseForm(ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ["exercise"]


class ExerciseSetForm(ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ["repetitions"]


WorkoutExerciseFormSet = inlineformset_factory(
    parent_model=Workout,
    model=WorkoutExercise,
    form=WorkoutExerciseForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=15,
    validate_max=True,
)

ExerciseSetFormSet = inlineformset_factory(
    parent_model=WorkoutExercise,
    model=ExerciseSet,
    form=ExerciseSetForm,
    extra=0,
    can_delete=True,
    min_num=1,
    validate_min=True,
    max_num=50,
    validate_max=True,
)
