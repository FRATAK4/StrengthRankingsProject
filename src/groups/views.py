import datetime
from datetime import timezone

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import GroupForm, GroupAddRequestForm
from .models import Group, GroupMembership, GroupAddRequest
from django.contrib.auth.models import User


class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_list.html"
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


class GroupCreateView(LoginRequiredMixin, CreateView):
    form_class = GroupForm
    template_name = "groups/group_create.html"

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.admin_user = self.request.user

        response = super().form_valid(form)

        GroupMembership.objects.create(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=self.request.user,
            group=self.object
        )

        return response

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "groups/group_detail.html"
    context_object_name = "group"

    def get_queryset(self):
        return Group.objects.filter(
            user_memberships__user=self.request.user,
            user_memberships__status=GroupMembership.MembershipStatus.ACCEPTED
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["host_view"] = (
            self.request.GET.get("host_view") == "true" and
            self.request.user == self.object.admin_user
        )
        context["member_count"] = GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            group=self.object
        ).count()
        return context

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "groups/group_edit.html"
    context_object_name = "group"

    def get_queryset(self):
        return Group.objects.filter(
            admin_user=self.request.user
        )

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.object.pk})

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = Group
    template_name = "groups/group_confirm_delete.html"

    def get_queryset(self):
        return self.request.user.groups_hosted.all()

    def get_success_url(self):
        return reverse_lazy("group_list")


class GroupUserKickView(LoginRequiredMixin, View):
    def post(self, request, pk, user_pk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=user_pk)

        if request.user != group.admin_user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=user, group=group)
        membership.status = GroupMembership.MembershipStatus.KICKED
        membership.kicked_at = datetime.datetime.now()
        membership.save()

        return redirect("group_user_list", pk=pk)

class GroupUserBlockView(View):
    def post(self, request, pk, user_pk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=user_pk)

        if request.user != group.admin_user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=user, group=group)
        membership.status = GroupMembership.MembershipStatus.BLOCKED
        membership.blocked_at = datetime.datetime.now()
        membership.save()

        return redirect("group_user_list", pk=pk)


class GroupRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = GroupAddRequest
    template_name = "groups/group_request_list.html"
    context_object_name = "requests"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def test_func(self):
        return self.request.user == self.group.admin_user

    def get_queryset(self):
        return GroupAddRequest.objects.filter(
            status=GroupAddRequest.RequestStatus.PENDING,
            group=self.group
        ).select_related("user")

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["request_count"] = context["requests"].count()
        return context


class GroupAcceptRequestView(LoginRequiredMixin, View):
    def post(self, request, pk, request_pk):
        group = get_object_or_404(Group, pk=pk)
        join_request = get_object_or_404(GroupAddRequest, pk=request_pk)

        if request.user != group.admin_user:
            return redirect("group_detail", pk=pk)

        join_request.status = GroupAddRequest.RequestStatus.ACCEPTED
        join_request.save()

        membership, created = GroupMembership.objects.get_or_create(
            user=join_request.user,
            group=group
        )

        membership.status=GroupMembership.MembershipStatus.ACCEPTED
        membership.save()

        return redirect("group_request_list", pk=pk)


class GroupDeclineRequestView(LoginRequiredMixin, View):
    def post(self, request, pk, request_pk):
        group = get_object_or_404(Group, pk=pk)
        join_request = get_object_or_404(
            GroupAddRequest,
            pk=request_pk,
        )

        if request.user != group.admin_user:
            return redirect("group_detail", pk=pk)

        join_request.status = GroupAddRequest.RequestStatus.DECLINED
        join_request.save()

        return redirect("group_request_list", pk=pk)


class GroupRankingsView(ListView):
    pass


class GroupUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "groups/group_user_list.html"
    context_object_name = "members"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def test_func(self):
        return GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=self.request.user,
            group=self.group
        ).exists()

    def get_queryset(self):
        return User.objects.filter(
            group_memberships__status=GroupMembership.MembershipStatus.ACCEPTED,
            group_memberships__group=self.group
        ).exclude(id=self.group.admin_user.id)

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["admin"] = self.group.admin_user
        context["host_view"] = (
            self.request.GET.get("host_view") == "true" and
            self.request.user == context["admin"]
        )
        return context

class GroupExitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        if request.user == group.admin_user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=request.user, group=group)
        membership.delete()

        return redirect("group_list")

class GroupSearchView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_search.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        return Group.objects.all().exclude(
            Q(
                user_memberships__user=self.request.user,
                user_memberships__status__in=[
                    GroupMembership.MembershipStatus.ACCEPTED,
                    GroupMembership.MembershipStatus.BLOCKED
                ]
            ) |
            Q(
                user_add_requests__user=self.request.user,
                user_add_requests__status=GroupAddRequest.RequestStatus.PENDING
            ) |
            Q(
                admin_user=self.request.user
            )
        )

class GroupSendRequestView(LoginRequiredMixin, CreateView):
    form_class = GroupAddRequestForm
    template_name = "groups/group_send_request.html"

    def setup(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("group_search")

    def form_valid(self, form):
        form.instance.status = GroupAddRequest.RequestStatus.PENDING
        form.instance.user = self.request.user
        form.instance.group = self.group

        return super().form_valid(form)





