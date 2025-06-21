from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import UserAndProfileFormView, LoggedUserProfileView, UserProfileView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(template_name="accounts/login.html"),
        name="accounts-login",
    ),
    path("logout/", LogoutView.as_view(), name="accounts-logout"),
    path("register/", UserAndProfileFormView.as_view(), name="accounts-register"),
    path("profile/", LoggedUserProfileView.as_view(), name="accounts-profile"),
    path(
        "profile/<slug:username>/",
        UserProfileView.as_view(),
        name="accounts-user_profile",
    ),
]
