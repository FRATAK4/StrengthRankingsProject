from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, TemplateView, RedirectView
from django.contrib.auth.models import User
from multi_form_view import MultiModelFormView  # type: ignore

from .forms import UserCreateForm, ProfileCreateForm


class UserAndProfileFormView(MultiModelFormView):
    form_classes = {
        "form_user": UserCreateForm,
        "form_profile": ProfileCreateForm,
    }
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts-login")

    def forms_valid(self, forms):
        a = forms["form_user"].save()
        b = forms["form_profile"].save(commit=False)
        b.user = a
        b.save()
        return super().forms_valid(forms)


class LoggedUserProfileView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self):
        return reverse(
            "accounts-user_profile", kwargs={"username": self.request.user.username}
        )


class UserProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "user_profile"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.select_related("profile")
