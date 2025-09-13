from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import Exists, Q, OuterRef, F
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView

from django.contrib.auth.models import User

from .forms import FriendRequestForm
from .models import Friendship, FriendRequest


class FriendDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "friendships/friend_dashboard.html"


class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_list.html"
    context_object_name = "friends"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            Q(
                sent_friendships__friend=self.request.user,
                sent_friendships__status=Friendship.FriendshipStatus.ACTIVE,
            )
            | Q(
                accepted_friendships__user=self.request.user,
                accepted_friendships__status=Friendship.FriendshipStatus.ACTIVE,
            )
        ).distinct()


class FriendKickView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend = get_object_or_404(User, pk=pk)
        friendship = Friendship.objects.filter(
            Q(status=Friendship.FriendshipStatus.ACTIVE),
            Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user),
        ).first()

        if not friendship:
            messages.error(request, "You can't kick this user!")
            return redirect("friend_list")

        Friendship.objects.filter(pk=friendship.pk).update(
            status=Friendship.FriendshipStatus.KICKED,
            kicked_at=timezone.now(),
            kicked_by=request.user,
        )

        messages.success(
            request, f"You successfully removed {friend.username} from your friends!"
        )
        return redirect("friend_list")


class FriendBlockView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        user_to_block = get_object_or_404(User, pk=pk)

        if request.user == user_to_block:
            messages.error(request, "You can't block yourself!")
            return redirect("friend_list")

        friendship = Friendship.objects.filter(
            Q(user=request.user, friend=user_to_block)
            | Q(user=user_to_block, friend=request.user)
        ).first()

        if not friendship:
            Friendship.objects.create(
                status=Friendship.FriendshipStatus.BLOCKED,
                user=request.user,
                friend=user_to_block,
                blocked_at=timezone.now(),
                blocked_by=request.user,
            )
        elif friendship.status == Friendship.FriendshipStatus.BLOCKED:
            messages.error(request, "You can't block this user!")
            return redirect("friend_list")
        else:
            friendship.status = Friendship.FriendshipStatus.BLOCKED
            friendship.blocked_at = timezone.now()
            friendship.blocked_by = request.user
            friendship.save()

        FriendRequest.objects.filter(
            Q(sender=request.user, receiver=user_to_block)
            | Q(sender=user_to_block, receiver=request.user),
            status=FriendRequest.RequestStatus.PENDING,
        ).update(status=FriendRequest.RequestStatus.DECLINED)

        messages.success(request, f"You successfully blocked {user_to_block.username}!")
        return redirect("friend_list")


class FriendRequestSentListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = "friendships/friend_request_sent_list.html"
    context_object_name = "requests_sent"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.model.objects.filter(
                status=FriendRequest.RequestStatus.PENDING, sender=self.request.user
            )
            .select_related("receiver", "receiver__profile")
            .order_by("-sent_at")
        )


class FriendRequestCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        request_sent = get_object_or_404(
            FriendRequest,
            pk=pk,
            sender=request.user,
            status=FriendRequest.RequestStatus.PENDING,
        )
        request_sent.delete()

        messages.success(request, "You successfully cancelled request!")
        return redirect("friend_request_sent_list")


class FriendRequestReceivedListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = "friendships/friend_request_received_list.html"
    context_object_name = "requests_received"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.model.objects.filter(
                status=FriendRequest.RequestStatus.PENDING, receiver=self.request.user
            )
            .select_related("sender", "sender__profile")
            .order_by("-sent_at")
        )


class FriendAcceptRequestView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        request_received = get_object_or_404(
            FriendRequest,
            pk=pk,
            receiver=request.user,
            status=FriendRequest.RequestStatus.PENDING,
        )
        request_received.status = FriendRequest.RequestStatus.ACCEPTED
        request_received.save()

        friendship = Friendship.objects.filter(
            Q(user=request_received.sender, friend=request_received.receiver)
            | Q(user=request_received.receiver, friend=request_received.sender)
        ).first()

        if not friendship:
            Friendship.objects.create(
                status=Friendship.FriendshipStatus.ACTIVE,
                user=request_received.sender,
                friend=request_received.receiver,
            )
        else:
            friendship.status = Friendship.FriendshipStatus.ACTIVE
            friendship.created_at = timezone.now()
            friendship.kicked_at = None
            friendship.blocked_at = None
            friendship.user = request_received.sender
            friendship.friend = request_received.receiver
            friendship.kicked_by = None
            friendship.blocked_by = None
            friendship.save()

        messages.success(
            request, f"You are now friend with {request_received.sender.username}!"
        )
        return redirect("friend_request_received_list")


class FriendDeclineRequestView(LoginRequiredMixin, View):
    def post(self, request, pk):
        request_received = get_object_or_404(
            FriendRequest,
            pk=pk,
            receiver=request.user,
            status=FriendRequest.RequestStatus.PENDING,
        )
        request_received.status = FriendRequest.RequestStatus.DECLINED
        request_received.save()

        messages.success(
            request, f"You declined request from {request_received.sender.username}!"
        )
        return redirect("friend_request_received_list")


class FriendBlockedListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_blocked_list.html"
    context_object_name = "friends_blocked"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            Q(
                sent_friendships__friend=self.request.user,
                sent_friendships__blocked_by=self.request.user,
            )
            | Q(
                accepted_friendships__user=self.request.user,
                accepted_friendships__blocked_by=self.request.user,
            )
        ).distinct()


class FriendUnblockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        friend = get_object_or_404(User, pk=pk)
        friendship = Friendship.objects.filter(
            Q(user=request.user) & Q(friend=friend) & Q(blocked_by=request.user)
            | Q(user=friend) & Q(friend=request.user) & Q(blocked_by=request.user)
        ).first()

        if not friendship:
            messages.error(request, "You can't unblock this user!")
            return redirect("friend_blocked_list")

        friendship.delete()

        messages.success(request, f"You successfully unblocked {friend.username}!")
        return redirect("friend_blocked_list")


class FriendBlockedByListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_blocked_by_list.html"
    context_object_name = "friends_blocked_by"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.filter(
            Q(
                sent_friendships__friend=self.request.user,
                sent_friendships__blocked_by=F("sent_friendships__user"),
            )
            | Q(
                accepted_friendships__user=self.request.user,
                accepted_friendships__blocked_by=F("accepted_friendships__friend"),
            )
        ).distinct()


class FriendSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_search.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.model.objects.exclude(pk=self.request.user.pk)
            .annotate(
                is_friend=Exists(
                    Friendship.objects.filter(
                        Q(status=Friendship.FriendshipStatus.ACTIVE),
                        Q(user=self.request.user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=self.request.user),
                    )
                ),
                request_sent_to=Exists(
                    FriendRequest.objects.filter(
                        status=FriendRequest.RequestStatus.PENDING,
                        sender=self.request.user,
                        receiver=OuterRef("pk"),
                    )
                ),
                request_sent_from=Exists(
                    FriendRequest.objects.filter(
                        status=FriendRequest.RequestStatus.PENDING,
                        sender=OuterRef("pk"),
                        receiver=self.request.user,
                    )
                ),
                blocked=Exists(
                    Friendship.objects.filter(
                        Q(blocked_by=self.request.user),
                        Q(user=self.request.user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=self.request.user),
                    )
                ),
                blocked_by=Exists(
                    Friendship.objects.filter(
                        Q(blocked_by=OuterRef("pk")),
                        Q(user=self.request.user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=self.request.user),
                    )
                ),
            )
            .distinct()
        )


class FriendSendRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = FriendRequestForm
    model = FriendRequest
    template_name = "friendships/friend_send_request.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Friend request sent to {self.friend.username}!"
        )
        return reverse_lazy("friend_search")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.friend = get_object_or_404(User, pk=kwargs.get("pk"))

    def test_func(self):
        is_user = self.request.user == self.friend

        has_friendship = Friendship.objects.filter(
            Q(
                status__in=[
                    Friendship.FriendshipStatus.BLOCKED,
                    Friendship.FriendshipStatus.ACTIVE,
                ]
            ),
            Q(user=self.request.user, friend=self.friend)
            | Q(user=self.friend, friend=self.request.user),
        ).exists()

        has_request = FriendRequest.objects.filter(
            Q(status=FriendRequest.RequestStatus.PENDING),
            Q(sender=self.request.user, receiver=self.friend)
            | Q(sender=self.friend, receiver=self.request.user),
        ).exists()

        return not (is_user or has_friendship or has_request)

    def handle_no_permission(self):
        messages.error(self.request, "You can't send request to this user!")
        return redirect("friend_search")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friend"] = self.friend
        return context

    def form_valid(self, form):
        form.instance.status = FriendRequest.RequestStatus.PENDING
        form.instance.sender = self.request.user
        form.instance.receiver = self.friend

        return super().form_valid(form)
