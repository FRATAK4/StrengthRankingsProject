from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Case, When, BooleanField, Exists, OuterRef
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    CreateView,
    TemplateView,
)

from groups.forms import GroupForm, GroupAddRequestForm
from groups.models import Group, GroupMembership, GroupAddRequest
from django.contrib.auth.models import User


class GroupUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "groups/group_functionality/group_user_list.html"
    context_object_name = "members"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def test_func(self):
        return GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=self.request.user,
            group=self.group,
        ).exists()

    def get_queryset(self):
        return (
            self.model.objects.filter(
                group_memberships__status=GroupMembership.MembershipStatus.ACCEPTED,
                group_memberships__group=self.group,
            )
            .exclude(id=self.group.admin_user.id)
            .select_related("profile")
        )

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["admin"] = self.group.admin_user
        context["is_admin"] = self.request.user == self.group.admin_user
        context["host_view"] = (
            self.request.GET.get("host_view") == "true"
            and self.request.user == context["admin"]
        )
        return context


class GroupUserKickView(LoginRequiredMixin, View):
    def post(self, request, pk, user_pk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=user_pk)

        if request.user != group.admin_user or request.user == user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(
            GroupMembership,
            user=user,
            group=group,
            status=GroupMembership.MembershipStatus.ACCEPTED,
        )
        membership.status = GroupMembership.MembershipStatus.KICKED
        membership.kicked_at = timezone.now()
        membership.save()

        url = reverse_lazy("group_user_list", kwargs={"pk": pk}) + "?host_view=true"
        return redirect(url)


class GroupUserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk, user_pk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=user_pk)

        if request.user != group.admin_user or request.user == user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=user, group=group)
        membership.status = GroupMembership.MembershipStatus.BLOCKED
        membership.blocked_at = timezone.now()
        membership.save()

        url = reverse_lazy("group_user_list", kwargs={"pk": pk}) + "?host_view=true"
        return redirect(url)


class GroupRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = GroupAddRequest
    template_name = "groups/group_functionality/group_request_list.html"
    context_object_name = "requests"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def test_func(self):
        return self.request.user == self.group.admin_user

    def get_queryset(self):
        return self.model.objects.filter(
            status=self.model.RequestStatus.PENDING, group=self.group
        ).select_related("user__profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
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
            group=group,
            defaults={"status": GroupMembership.MembershipStatus.ACCEPTED},
        )
        if not created:
            membership.status = GroupMembership.MembershipStatus.ACCEPTED
            membership.kicked_at = None
            membership.blocked_at = None
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


class GroupRankingsView(TemplateView):
    template_name = "groups/group_functionality/group_rankings.html"


class GroupExitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        if request.user == group.admin_user:
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=request.user, group=group)
        membership.delete()

        return redirect("group_dashboard")


class GroupSearchView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_functionality/group_search.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.with_member_count().annotate(
            is_admin=Case(
                When(admin_user=self.request.user, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            is_member=Exists(
                GroupMembership.objects.filter(
                    status=GroupMembership.MembershipStatus.ACCEPTED,
                    user=self.request.user,
                    group=OuterRef("pk"),
                )
            ),
            is_blocked=Exists(
                GroupMembership.objects.filter(
                    status=GroupMembership.MembershipStatus.BLOCKED,
                    user=self.request.user,
                    group=OuterRef("pk"),
                )
            ),
            is_pending=Exists(
                GroupAddRequest.objects.filter(
                    status=GroupAddRequest.RequestStatus.PENDING,
                    user=self.request.user,
                    group=OuterRef("pk"),
                )
            ),
        )


class GroupSendRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = GroupAddRequestForm
    model = GroupAddRequest
    template_name = "groups/group_functionality/group_send_request.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["group"] = self.group

        return context

    def get_success_url(self):
        return reverse_lazy("group_search")

    def test_func(self):
        return not GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.BLOCKED,
            user=self.request.user,
            group=self.group,
        ).exists()

    def form_valid(self, form):
        form.instance.status = GroupAddRequest.RequestStatus.PENDING
        form.instance.user = self.request.user
        form.instance.group = self.group

        return super().form_valid(form)
