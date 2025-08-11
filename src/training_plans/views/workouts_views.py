from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    View,
    DeleteView,
)

from training_plans.forms import (
    TrainingPlanForm,
    WorkoutForm,
    WorkoutExerciseFormSet,
    ExerciseSetFormSet,
)
from training_plans.models import TrainingPlan, Workout


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    form_class = WorkoutForm
    template_name = "training_plans/workouts/workout_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["training_plan"] = get_object_or_404(
            TrainingPlan, pk=self.kwargs.get("pk")
        )
        context["day"] = self.request.GET.get("day")
        return context

    def get_success_url(self):
        return reverse(
            "workout_edit",
            kwargs={
                "training_plan_pk": self.object.training_plan.pk,
                "workout_pk": self.object.pk,
            },
        )

    def form_valid(self, form):
        messages.success(self.request, "Workout created successfully!")
        context = self.get_context_data()
        training_plan_instance = context["training_plan"]
        day = context["day"]
        workout = form.save(commit=False)
        workout.training_plan = training_plan_instance
        workout.day = day
        workout.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't create workout")
        return super().form_invalid(form)


class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = "training_plans/workouts/workout_detail.html"
    context_object_name = "workout"
    pk_url_kwarg = "workout_pk"

    def get_queryset(self):
        return Workout.objects.prefetch_related("exercises__exercise_sets")


class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    form_class = WorkoutForm
    template_name = "training_plans/workouts/workout_update.html"
    pk_url_kwarg = "workout_pk"

    def get_success_url(self):
        return reverse(
            "workout_edit",
            kwargs={
                "training_plan_pk": self.object.training_plan.pk,
                "workout_pk": self.object.pk,
            },
        )

    def form_valid(self, form):
        messages.success(self.request, "Workout updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't update workout")
        return super().form_invalid(form)


class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = "training_plans/workouts/workout_confirm_delete.html"
    pk_url_kwarg = "workout_pk"

    def get_success_url(self):
        return reverse(
            "training_plan_detail", kwargs={"pk": self.kwargs.get("training_plan_pk")}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Successfully deleted workout!")
        super().delete(request, *args, **kwargs)


class WorkoutFormSetView(LoginRequiredMixin, View):
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
            self.request, "training_plans/workouts/workout_exercises_form.html", context
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
                return redirect(
                    "workout_detail",
                    training_plan_pk=self.training_plan.pk,
                    workout_pk=self.workout.pk,
                )
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
            self.request, "training_plans/workouts/workout_exercises_form.html", context
        )
