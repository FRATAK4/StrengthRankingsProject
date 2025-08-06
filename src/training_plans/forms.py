from django.forms.models import ModelForm, inlineformset_factory
from .models import TrainingPlan, Workout, WorkoutExercise, ExerciseSet


class TrainingPlanForm(ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ["name", "description"]


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
