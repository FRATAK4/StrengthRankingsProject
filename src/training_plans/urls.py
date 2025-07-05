from django.urls import path
from . import views

# from .views import (
#     UserTrainingPlanListView,
#     TrainingPlanListView,
#     TrainingPlanDetailView,
#     TrainingPlanCreateView,
#     TrainingPlanRatingListView,
#     TrainingPlanRatingDetailView,
#     WorkoutDetailView,
# )

urlpatterns = [
    path(
        "create/", views.TrainingPlanCreateView.as_view(), name="training_plan_create"
    ),
    path(
        "<int:pk>/edit/",
        views.TrainingPlanUpdateView.as_view(),
        name="edit_training_plan",
    ),
    path(
        "<int:pk>/detail/",
        views.TrainingPlanDetailView.as_view(),
        name="training_plan_detail",
    ),
    # path("", TrainingPlanListView.as_view(), name="training_plans"),
    # path("user/", UserTrainingPlanListView.as_view(), name="training_plans-user"),
    # path("<int:pk>/", TrainingPlanDetailView.as_view(), name="training_plan"),
    # path(
    #     "workouts/<int:pk>", WorkoutDetailView.as_view(), name="training_plan-workout"
    # ),
    # path("create/", TrainingPlanCreateView.as_view(), name="training_plan-create"),
    # path(
    #     "<int:pk>/ratings/",
    #     TrainingPlanRatingListView.as_view(),
    #     name="training_plan-ratings",
    # ),
    # path(
    #     "<int:pk>/ratings/<int:pk_rating>/",
    #     TrainingPlanRatingDetailView.as_view(),
    #     name="training_plan-rating",
    # ),
]
