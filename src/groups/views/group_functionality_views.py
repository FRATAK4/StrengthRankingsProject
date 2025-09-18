from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Case, When, BooleanField, Exists, OuterRef, Q
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

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You must be a member of this group to view its members.",
        )
        return redirect("group_detail", pk=self.group.pk)

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

        if request.user != group.admin_user:
            messages.error(request, "Only the group admin can kick members.")
            return redirect("group_detail", pk=pk)

        if request.user == user:
            messages.error(request, "You cannot kick yourself from the group.")
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

        messages.success(
            request,
            f"{user.username} has been kicked from the group.",
        )

        url = reverse_lazy("group_user_list", kwargs={"pk": pk}) + "?host_view=true"
        return redirect(url)


class GroupUserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk, user_pk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=user_pk)

        if request.user != group.admin_user:
            messages.error(request, "Only the group admin can block members.")
            return redirect("group_detail", pk=pk)

        if request.user == user:
            messages.error(request, "You cannot block yourself.")
            return redirect("group_detail", pk=pk)

        membership = get_object_or_404(GroupMembership, user=user, group=group)
        membership.status = GroupMembership.MembershipStatus.BLOCKED
        membership.blocked_at = timezone.now()
        membership.save()

        messages.warning(
            request,
            f"{user.username} has been blocked from the group.",
        )

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

    def handle_no_permission(self):
        messages.error(
            self.request,
            "Only the group admin can manage join requests.",
        )
        return redirect("group_detail", pk=self.group.pk)

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
            messages.error(request, "Only the group admin can accept join requests.")
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

        messages.success(
            request,
            f"{join_request.user.username} has been accepted into the group!",
        )

        return redirect("group_request_list", pk=pk)


class GroupDeclineRequestView(LoginRequiredMixin, View):
    def post(self, request, pk, request_pk):
        group = get_object_or_404(Group, pk=pk)
        join_request = get_object_or_404(
            GroupAddRequest,
            pk=request_pk,
        )

        if request.user != group.admin_user:
            messages.error(request, "Only the group admin can decline join requests.")
            return redirect("group_detail", pk=pk)

        join_request.status = GroupAddRequest.RequestStatus.DECLINED
        join_request.save()

        messages.info(
            request,
            f"Join request from {join_request.user.username} has been declined.",
        )

        return redirect("group_request_list", pk=pk)


class GroupBlockedUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "groups/group_functionality/group_user_blocked_list.html"
    context_object_name = "blocked_users"
    paginate_by = 10

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))

    def test_func(self):
        return self.request.user == self.group.admin_user

    def handle_no_permission(self):
        messages.error(self.request, "Only the group admin can view blocked users.")
        return redirect("group_detail", pk=self.group.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["group"] = self.group
        context["admin"] = self.group.admin_user
        return context

    def get_queryset(self):
        return (
            self.model.objects.filter(
                group_memberships__status=GroupMembership.MembershipStatus.BLOCKED,
                group_memberships__group=self.group,
            )
            .select_related("profile")
            .prefetch_related("group_memberships")
        )


class GroupUnblockUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.group = get_object_or_404(Group, pk=kwargs.get("pk"))
        self.user_to_unblock = get_object_or_404(User, pk=kwargs.get("user_pk"))

    def test_func(self):
        return self.request.user == self.group.admin_user

    def handle_no_permission(self):
        messages.error(self.request, "Only the group admin can unblock users.")
        return redirect("group_detail", pk=self.group.pk)

    def post(self, request, *args, **kwargs):
        membership = GroupMembership.objects.filter(
            user=self.user_to_unblock,
            group=self.group,
            status=GroupMembership.MembershipStatus.BLOCKED,
        ).first()

        if membership:
            membership.delete()
            messages.success(
                request, f"{self.user_to_unblock.username} has been unblocked."
            )
        else:
            messages.warning(
                request,
                f"{self.user_to_unblock.username} is not blocked in this group.",
            )

        return redirect("group_user_blocked_list", pk=self.group.pk)


class GroupRankingsView(TemplateView):
    template_name = "groups/group_functionality/group_rankings.html"


class GroupExitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)

        if request.user == group.admin_user:
            messages.error(
                request,
                "Admin cannot leave a group.",
            )
            return redirect("group_detail", pk=pk)

        membership = GroupMembership.objects.filter(
            user=request.user, group=group
        ).first()

        if membership:
            membership.delete()
            messages.success(
                request,
                f"You have successfully left '{group.name}'.",
            )
        else:
            messages.warning(
                request,
                "You are not a member of this group.",
            )

        return redirect("group_dashboard")


class GroupSearchView(LoginRequiredMixin, ListView):
    model = Group
    template_name = "groups/group_functionality/group_search.html"
    context_object_name = "groups"
    paginate_by = 10

    def get_queryset(self):
        queryset = self.model.objects.with_member_count().annotate(
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

        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(admin_user__username__icontains=search_query)
            )

        return queryset


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
        blocked = GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.BLOCKED,
            user=self.request.user,
            group=self.group,
        ).exists()

        is_member = GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=self.request.user,
            group=self.group,
        ).exists()

        has_pending = GroupAddRequest.objects.filter(
            status=GroupAddRequest.RequestStatus.PENDING,
            user=self.request.user,
            group=self.group,
        ).exists()

        return not blocked and not is_member and not has_pending

    def handle_no_permission(self):
        if GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.BLOCKED,
            user=self.request.user,
            group=self.group,
        ).exists():
            messages.error(
                self.request,
                "You are blocked from this group.",
            )
        elif GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED,
            user=self.request.user,
            group=self.group,
        ).exists():
            messages.info(
                self.request,
                "You are already a member of this group.",
            )
        elif GroupAddRequest.objects.filter(
            status=GroupAddRequest.RequestStatus.PENDING,
            user=self.request.user,
            group=self.group,
        ).exists():
            messages.info(
                self.request,
                "You already have a pending request for this group.",
            )

        return redirect("group_search")

    def form_valid(self, form):
        form.instance.status = GroupAddRequest.RequestStatus.PENDING
        form.instance.user = self.request.user
        form.instance.group = self.group

        response = super().form_valid(form)

        messages.success(
            self.request, f"Your join request for '{self.group.name}' has been sent! "
        )

        return response
