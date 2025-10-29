from typing import Any, cast
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q, Count, QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from groups.forms import GroupForm
from groups.models import Group, GroupMembership, GroupAddRequest


class GroupDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "groups/group_crud/group_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = cast(User, self.request.user)
        context = super().get_context_data(**kwargs)

        groups_hosted = user.groups_hosted.with_member_count()

        groups_joined = (
            Group.objects.with_member_count()
            .filter(
                user_memberships__status=GroupMembership.MembershipStatus.ACCEPTED,
                user_memberships__user=user,
            )
            .exclude(admin_user=user)
        )

        groups_blocked = Group.objects.with_member_count().filter(
            user_memberships__status=GroupMembership.MembershipStatus.BLOCKED,
            user_memberships__user=user,
        )

        groups_pending = Group.objects.with_member_count().filter(
            user_add_requests__status=GroupAddRequest.RequestStatus.PENDING,
            user_add_requests__user=user,
        )

        context["groups_hosted"] = groups_hosted
        context["groups_joined"] = groups_joined
        context["groups_blocked"] = groups_blocked
        context["groups_pending"] = groups_pending

        return context


class GroupCreateView(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    template_name = "groups/group_crud/group_create.html"
    object: Group

    def get_success_url(self) -> str:
        return reverse("group_detail", kwargs={"pk": self.object.pk})

    @transaction.atomic
    def form_valid(self, form: GroupForm) -> HttpResponse:
        user = cast(User, self.request.user)
        form.instance.admin_user = user

        response = super().form_valid(form)

        GroupMembership.objects.create(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=user,
            group=self.object,
        )

        messages.success(
            self.request,
            f"Group '{self.object.name}' created successfully!",
        )

        return response


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "groups/group_crud/group_detail.html"
    context_object_name = "group"

    def get_queryset(self) -> QuerySet[Group]:
        user = cast(User, self.request.user)
        return (
            self.model.objects.with_member_count()
            .filter(
                user_memberships__user=user,
                user_memberships__status=GroupMembership.MembershipStatus.ACCEPTED,
            )
            .annotate(
                pending_requests=Count(
                    "user_add_requests",
                    filter=Q(
                        user_add_requests__status=GroupAddRequest.RequestStatus.PENDING
                    ),
                ),
                blocked_users_count=Count(
                    "user_memberships",
                    filter=Q(
                        user_memberships__status=GroupMembership.MembershipStatus.BLOCKED
                    ),
                ),
            )
            .select_related("admin_user__profile")
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = cast(User, self.request.user)
        context = super().get_context_data(**kwargs)

        is_admin = user == self.object.admin_user

        context["is_admin"] = is_admin
        context["host_view"] = self.request.GET.get("host_view") == "true" and is_admin

        return context


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/group_crud/group_edit.html"
    context_object_name = "group"

    def get_queryset(self) -> QuerySet[Group]:
        user = cast(User, self.request.user)
        return self.model.objects.filter(admin_user=user)

    def get_success_url(self) -> str:
        return reverse("group_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form: GroupForm) -> HttpResponse:
        messages.success(
            self.request,
            f"Group '{self.object.name}' updated successfully!",
        )
        return super().form_valid(form)

    def form_invalid(self, form: GroupForm) -> HttpResponse:
        messages.error(
            self.request,
            "There was an error updating the group.",
        )
        return super().form_invalid(form)


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_crud/group_confirm_delete.html"

    def get_queryset(self) -> QuerySet[Group]:
        user = cast(User, self.request.user)
        return user.groups_hosted.all()

    def get_success_url(self) -> str:
        return reverse("group_dashboard")

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        group_name = self.get_object().name
        response = super().delete(request, *args, **kwargs)
        messages.success(
            request,
            f"Group '{group_name}' has been deleted.",
        )
        return response
