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
            "workout_exercises_manage",
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

    def get_queryset(self):
        training_plan = get_object_or_404(
            TrainingPlan, pk=self.kwargs.get("training_plan_pk")
        )
        return Workout.objects.filter(training_plan=training_plan)

    def get_success_url(self):
        return reverse(
            "workout_edit_exercises",
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


class WorkoutExercisesManageView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.training_plan = get_object_or_404(
            TrainingPlan, pk=kwargs.get("training_plan_pk")
        )
        self.workout = get_object_or_404(Workout, pk=kwargs.get("workout_pk"))
        self.is_editing = self.workout.exercises.exists()

    def get_formsets(self, data=None):
        workout_exercise_formset = WorkoutExerciseFormSet(
            data, instance=self.workout, prefix="exercises"
        )

        exercise_set_formsets = []
        for i, workout_exercise_form in enumerate(workout_exercise_formset.forms):
            formset = ExerciseSetFormSet(
                data,
                instance=workout_exercise_form.instance,
                prefix=f"sets-{i}"
            )
            exercise_set_formsets.append(formset)

        return workout_exercise_formset, exercise_set_formsets

    def get(self, request, *args, **kwargs):
        workout_exercise_formset, exercise_set_formsets = self.get_formsets()

        context = {
            "training_plan": self.training_plan,
            "workout": self.workout,
            "workout_exercise_formset": workout_exercise_formset,
            "exercise_set_formsets": exercise_set_formsets,
            "is_editing": self.is_editing,
        }

        return render(
            self.request, "training_plans/workouts/workout_exercises_manage.html", context
        )

    def post(self, request, *args, **kwargs):
        workout_exercise_formset, exercise_set_formsets = self.get_formsets(request.POST)

        if workout_exercise_formset.is_valid():
            workout_exercise_formset.save()

            all_valid = all(
                exercise_set_formset.is_valid()
                for exercise_set_formset in exercise_set_formsets
            )

            if all_valid:
                for exercise_set_formset in exercise_set_formsets:
                    sets = exercise_set_formset.save(commit=False)
                    for j, set_obj in enumerate(sets):
                        set_obj.set_number = j + 1
                        set_obj.save()
                    exercise_set_formset.save_m2m()

                action = "updated" if self.is_editing else "created"
                messages.success(request, f"Workout exercises {action} successfully!")

                return redirect(
                    "workout_detail",
                    training_plan_pk=self.training_plan.pk,
                    workout_pk=self.workout.pk,
                )

        context = {
            "training_plan": self.training_plan,
            "workout": self.workout,
            "workout_exercise_formset": workout_exercise_formset,
            "exercise_set_formsets": exercise_set_formsets,
            "is_editing": self.is_editing,
        }

        return render(
            request, "training_plans/workouts/workout_exercises_manage.html", context
        )
