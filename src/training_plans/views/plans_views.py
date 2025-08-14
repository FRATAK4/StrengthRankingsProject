from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from training_plans.forms import (
    TrainingPlanForm,
    WorkoutForm,
    WorkoutExerciseFormSet,
    ExerciseSetFormSet,
)
from training_plans.models import TrainingPlan, Workout
from django.db.models import Avg


class TrainingPlanListView(LoginRequiredMixin, ListView):
    model = TrainingPlan
    template_name = "training_plans/plans/training_plan_list.html"
    context_object_name = "training_plans"

    def get_queryset(self):
        return TrainingPlan.objects.filter(user=self.request.user)


class TrainingPlanCreateView(LoginRequiredMixin, CreateView):
    form_class = TrainingPlanForm
    template_name = "training_plans/plans/training_plan_create.html"

    def get_success_url(self):
        return reverse("training_plan_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Training plan created successfully!")
        training_plan = form.save(commit=False)
        training_plan.user = self.request.user
        training_plan.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't create training plan!")
        return super().form_invalid(form)


class TrainingPlanDetailView(LoginRequiredMixin, DetailView):
    model = TrainingPlan
    template_name = "training_plans/plans/training_plan_detail.html"
    context_object_name = "training_plan"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("workouts", "workouts__exercises")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Create a dictionary of workouts by day
        workouts_by_day = {}
        for workout in self.object.workouts.all():
            workouts_by_day[workout.day] = workout

        # Days of the week
        days = [
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ]

        # Calculate total exercises
        total_exercises = sum(
            workout.exercises.count() for workout in self.object.workouts.all()
        )

        # Calculate average rating
        avg_rating = self.object.user_ratings.aggregate(Avg("rating"))["rating__avg"]

        context.update(
            {
                "workouts_by_day": workouts_by_day,
                "days": days,
                "total_exercises": total_exercises,
                "avg_rating": avg_rating,
            }
        )

        return context


class TrainingPlanUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TrainingPlanForm
    template_name = "training_plans/plans/training_plan_update.html"

    def get_queryset(self):
        return TrainingPlan.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse("training_plan_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Training plan updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Couldn't update training plan!")
        return super().form_invalid(form)


class TrainingPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = TrainingPlan
    template_name = "training_plans/plans/training_plan_confirm_delete.html"
    success_url = reverse_lazy("training_plan_list")

    def get_queryset(self):
        return TrainingPlan.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Successfully deleted training plan!")
        super().delete(request, *args, **kwargs)
