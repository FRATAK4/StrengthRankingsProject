from django.shortcuts import render
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User

from .forms import UserCreateForm


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "accounts/register.html"


class UserProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("profile")
        return queryset
