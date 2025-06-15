from django.shortcuts import render
from django.views.generic import ListView, DetailView

from src.exercises.models import Exercise


class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercises/exercise_list.html"


class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = "exercises/exercise.html"
