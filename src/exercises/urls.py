from django.urls import path

from src.exercises.views import ExerciseListView, ExerciseDetailView

urlpatterns = [
    path("", ExerciseListView.as_view(), name="exercises-list"),
    path("<int:pk>", ExerciseDetailView.as_view(), name="exercises-detail"),
]
