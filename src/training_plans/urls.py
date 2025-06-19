from django.urls import path

from src.training_plans.views import UserTrainingPlansListView, TrainingPlansListView

urlpatterns = [
    path("", TrainingPlansListView.as_view(), name="training_plans"),
    path("user/", UserTrainingPlansListView.as_view(), name="training_plans-user"),
]
