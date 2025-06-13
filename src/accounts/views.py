from django.shortcuts import render
from django.views.generic import CreateView

from .forms import UserCreateForm


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = "accounts/register.html"
