from django.contrib.auth.views import LoginView
from django.urls import path

from .views import UserCreateView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="accounts/login.html"),
        name="accounts-login",
    ),
    path("register/", UserCreateView.as_view(), name="accounts-register"),
]
