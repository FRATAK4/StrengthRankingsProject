from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
)

from .forms import (
    TrainingPlanForm,
    WorkoutForm,
    WorkoutExerciseFormSet,
    ExerciseSetFormSet,
)
from .models import TrainingPlan, Workout


class TrainingPlanListView(ListView):
    model = TrainingPlan
    template_name = "training_plans/training_plan_list.html"
    context_object_name = "training_plans"

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get("pk"))
        return TrainingPlan.objects.filter(user=user)


class TrainingPlanCreateView(CreateView):
    form_class = TrainingPlanForm
    template_name = "training_plans/training_plan_create.html"

    def form_valid(self, form):
        messages.success(self.request, "Training plan created successfully!")
        training_plan = form.save(commit=False)
        training_plan.user = self.request.user
        training_plan.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't create training plan!")
        return super().form_invalid(form)


class TrainingPlanDetailView(DetailView):
    model = TrainingPlan
    template_name = "training_plans/training_plan_detail.html"
    context_object_name = "training_plan"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("workouts")


class TrainingPlanUpdateView(UpdateView):
    form_class = TrainingPlanForm
    template_name = "training_plans/training_plan_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Training plan updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't update training plan!")
        return super().form_invalid(form)


class TrainingPlanDeleteView(DeleteView):
    model = TrainingPlan
    template_name = "training_plans/training_plan_confirm_delete.html"
    success_url = reverse_lazy("")

    def delete(self, request, *args, **kwargs):
        messages.error(request, "Successfully deleted training plan!")
        super().delete(request, *args, **kwargs)


class WorkoutCreateView(CreateView):
    form_class = WorkoutForm
    template_name = "training_plans/workout_create.html"

    def form_valid(self, form):
        messages.success(self.request, "Workout created successfully!")
        training_plan_instance = get_object_or_404(
            TrainingPlan, pk=self.kwargs.get("pk")
        )
        workout = form.save(commit=False)
        workout.training_plan = training_plan_instance
        workout.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't create workout")


class WorkoutFormSetView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.training_plan = get_object_or_404(
            TrainingPlan, pk=kwargs.get("training_plan_pk")
        )
        self.workout = get_object_or_404(Workout, pk=kwargs.get("workout_pk"))

    def get(self):
        workout_exercise_formset = WorkoutExerciseFormSet(
            instance=self.workout, prefix="exercises"
        )
        exercise_set_formsets = []

        for i, form in enumerate(workout_exercise_formset.forms):
            workout_exercise_instance = form.instance
            formset = ExerciseSetFormSet(
                instance=workout_exercise_instance, prefix=f"sets-{i}"
            )
            exercise_set_formsets.append(formset)

        context = {
            "training_plan": self.training_plan,
            "workout": self.workout,
            "workout_exercise_formset": workout_exercise_formset,
            "exercise_set_formsets": exercise_set_formsets,
        }

        return render(
            self.request, "training_plans/workout_exercises_form.html", context
        )

    def post(self):
        workout_exercise_formset = WorkoutExerciseFormSet(
            self.request.POST, instance=self.workout, prefix="exercises"
        )
        exercise_set_formsets = []

        if workout_exercise_formset.is_valid():
            workout_exercise_formset.save()
            for i, workout_exercise_form in enumerate(workout_exercise_formset.forms):
                exercise_set_formset = ExerciseSetFormSet(
                    self.request.POST,
                    instance=workout_exercise_form.instance,
                    prefix=f"sets-{i}",
                )
                exercise_set_formsets.append(exercise_set_formset)

            all_valid = all(
                exercise_set_formset.is_valid()
                for exercise_set_formset in exercise_set_formsets
            )
            if all_valid:
                for exercise_set_formset in exercise_set_formsets:
                    exercise_set_formset.save()
                return redirect("my-url")
        else:
            for i, form in enumerate(workout_exercise_formset.forms):
                formset = ExerciseSetFormSet(
                    self.request.POST, instance=form.instance, prefix=f"sets-{i}"
                )
                exercise_set_formsets.append(formset)

        context = {
            "training_plan": self.training_plan,
            "workout": self.workout,
            "workout_exercise_formset": workout_exercise_formset,
            "exercise_set_formsets": list(
                zip(workout_exercise_formset.forms, exercise_set_formsets)
            ),
        }

        return render(
            self.request, "training_plans/workout_exercises_form.html", context
        )


class WorkoutDetailView(DetailView):
    model = Workout
    template_name = "training_plans/workout_detail.html"
    context_object_name = "workout"

    def get_queryset(self):
        return Workout.objects.prefetch_related("exercises__exercise_sets")


class WorkoutUpdateView(UpdateView):
    form_class = WorkoutForm
    template_name = "training_plans/workout_update.html"

    def form_valid(self, form):
        messages.success(self.request, "Workout updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't update workout")
        return super().form_invalid(form)
