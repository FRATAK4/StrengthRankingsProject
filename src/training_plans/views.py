from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .forms import TrainingPlanCreateForm, TrainingPlanRatingCreateForm
from .models import TrainingPlan, Workout, TrainingPlanRating


class TrainingPlanListView(ListView):
    model = TrainingPlan
    template_name = "training_plans/training_plans_list.html"


class UserTrainingPlanListView(ListView):
    model = TrainingPlan
    template_name = "training_plans/user_training_plans_list.html"


class TrainingPlanDetailView(DetailView):
    model = TrainingPlan
    template_name = "training_plans/training_plan.html"


class WorkoutDetailView(DetailView):
    model = Workout
    template_name = "training_plans/workout.html"


class TrainingPlanCreateView(CreateView):
    form_class = TrainingPlanCreateForm
    template_name = "training_plans/training_plan_create.html"


class TrainingPlanRatingListView(DetailView):
    model = TrainingPlan
    template_name = "training_plans/training_plan_rating_list.html"


class TrainingPlanRatingDetailView(DetailView):
    model = TrainingPlanRating
    template_name = "training_plans/training_plan_rating.html"


class TrainingPlanRatingCreateView(CreateView):
    form_class = TrainingPlanRatingCreateForm
    template_name = "training_plans/training_plan_rating_create.html"
