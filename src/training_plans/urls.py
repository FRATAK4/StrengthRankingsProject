from django.urls import path

from .views.plans_views import (
    TrainingPlanListView,
    TrainingPlanCreateView,
    TrainingPlanDetailView,
    TrainingPlanUpdateView,
    TrainingPlanDeleteView,
)
from .views.workouts_views import (
    WorkoutCreateView,
    WorkoutDetailView,
    WorkoutUpdateView,
    WorkoutFormSetView,
    WorkoutDeleteView,
)

urlpatterns = [
    path("", TrainingPlanListView.as_view(), name="training_plan_list"),
    path("create/", TrainingPlanCreateView.as_view(), name="training_plan_create"),
    path("<int:pk>/", TrainingPlanDetailView.as_view(), name="training_plan_detail"),
    path("<int:pk>/edit/", TrainingPlanUpdateView.as_view(), name="training_plan_edit"),
    path(
        "<int:pk>/delete/",
        TrainingPlanDeleteView.as_view(),
        name="training_plan_delete",
    ),
    path("<int:pk>/create/", WorkoutCreateView.as_view(), name="workout_create"),
    path(
        "<int:training_plan_pk>/<int:workout_pk>/",
        WorkoutDetailView.as_view(),
        name="workout_detail",
    ),
    path(
        "<int:training_plan_pk>/<int:workout_pk>/edit",
        WorkoutUpdateView.as_view(),
        name="workout_edit",
    ),
    path(
        "<int:training_plan_pk>/<int:workout_pk>/delete",
        WorkoutDeleteView.as_view(),
        name="workout_delete",
    ),
    path(
        "<int:training_plan_pk>/<int:workout_pk>/edit_exercises",
        WorkoutFormSetView.as_view(),
        name="workout_edit_exercises",
    ),
]
