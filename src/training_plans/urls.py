from django.urls import path

from src.training_plans.views import (
    UserTrainingPlanListView,
    TrainingPlanListView,
    TrainingPlanDetailView,
    TrainingPlanCreateView,
    TrainingPlanRatingListView,
    TrainingPlanRatingDetailView,
    TrainingPlanRatingCreateView,
    WorkoutDetailView,
)

urlpatterns = [
    path("", TrainingPlanListView.as_view(), name="training_plans"),
    path("user/", UserTrainingPlanListView.as_view(), name="training_plans-user"),
    path("<int:pk>/", TrainingPlanDetailView.as_view(), name="training_plan"),
    path(
        "workouts/<int:pk>", WorkoutDetailView.as_view(), name="training_plan-workout"
    ),
    path("create/", TrainingPlanCreateView.as_view(), name="training_plan-create"),
    path(
        "<int:pk>/ratings/",
        TrainingPlanRatingListView.as_view(),
        name="training_plan-ratings",
    ),
    path(
        "<int:pk>/ratings/<int:pk_rating>/",
        TrainingPlanRatingDetailView.as_view(),
        name="training_plan-rating",
    ),
    path(
        "<int:pk>/ratings/create/",
        TrainingPlanRatingCreateView.as_view(),
        name="training_plan-rating_create",
    ),
]
