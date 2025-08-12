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
        widgets = {"exercise": forms.Select(attrs={"class": "form-select"})}


class ExerciseSetForm(ModelForm):
    set_number = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = ExerciseSet
        fields = ["set_number", "repetitions"]
        widgets = {
            "repetitions": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "100",
                    "placeholder": "10",
                }
            )
        }


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
