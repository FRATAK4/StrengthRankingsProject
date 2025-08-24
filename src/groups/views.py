from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import GroupForm
from .models import Group, GroupMembership, GroupAddRequest
from django.contrib.auth.models import User


class GroupDashboardView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_dashboard.html"
    context_object_name = "groups"

    def get_queryset(self):
        return Group.objects.none()

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data()

        groups_hosted = self.request.user.groups_hosted.all()
        groups_joined = Group.objects.filter(
            user_memberships__user=self.request.user,
            user_memberships__status=GroupMembership.MembershipStatus.ACCEPTED
        ).exclude(admin_user=self.request.user)

        context["groups_hosted"] = groups_hosted
        context["groups_joined"] = groups_joined

        return context


class GroupCreateView(CreateView):
    form_class = GroupForm
    template_name = "groups/group_create.html"

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        group = form.save(commit=False)
        group.admin_user = self.request.user
        group.save()
        membership = GroupMembership(status="accepted", user=self.request.user, group=group)
        membership.save()
        return super().form_valid(form)

class GroupDetailView(DetailView):
    model = Group
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def get_queryset(self):
        return self.request.user.group_memberships.filter(status="accepted").values_list("group", flat=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["host_view"] = self.request.GET.get("host_view")
        return context

class GroupUpdateView(UpdateView):
    form_class = GroupForm
    template_name = "groups/group_edit.html"

    def get_queryset(self):
        return self.request.user.group_memberships.filter(status="accepted").values_list("group", flat=True)

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.object.pk})

class GroupDeleteView(DeleteView):
    model = Group
    template_name = "groups/group_confirm_delete.html"

    def get_queryset(self):
        return self.request.user.groups_hosted.all()

    def get_success_url(self):
        return reverse("group_list")


class GroupUserKickView(View):
    pass


class GroupUserBlockView(View):
    pass


class GroupRequestListView(ListView):
    model = GroupAddRequest
    template_name = "groups/group_request_list.html"

    def get_queryset(self):
        group_pk = self.kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_pk)
        return group.user_add_requests.filter(status="pending")



class GroupAcceptRequestView(View):
    pass


class GroupDeclineRequestView(View):
    pass


class GroupRankingsView(ListView):
    pass


class GroupUserListView(ListView):
    model = User
    template_name = "groups/group_user_list.html"

    def get_queryset(self):
        group_pk = self.kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_pk)
        return group.user_memberships.filter(status="accepted").values_list("user", flat=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["host_view"] = self.request.GET.get("host_view")
        return context


class GroupExitView(DeleteView):
    pass


class GroupSearchView(ListView):
    pass


class GroupSendRequestView(View):
    pass
