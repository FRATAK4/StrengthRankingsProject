from typing import Any, cast

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import Exists, Q, OuterRef, F, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView

from django.contrib.auth.models import User

from .forms import FriendRequestForm
from .models import Friendship, FriendRequest
from notifications.models import Notification


class FriendDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "friendships/friend_dashboard.html"


class FriendListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_list.html"
    context_object_name = "friends"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[User]:
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
    @transaction.atomic
    def post(self, request: HttpRequest, pk: str) -> HttpResponseRedirect:
        user = cast(User, request.user)

        friend = get_object_or_404(User, pk=pk)
        friendship = Friendship.objects.filter(
            Q(status=Friendship.FriendshipStatus.ACTIVE),
            Q(user=user, friend=friend) | Q(user=friend, friend=user),
        ).first()

        if not friendship:
            messages.error(request, "You can't kick this user!")
            return redirect("friend_list")

        Friendship.objects.filter(pk=friendship.pk).update(
            status=Friendship.FriendshipStatus.KICKED,
            kicked_at=timezone.now(),
            kicked_by=user,
        )

        Notification.objects.create(
            type=Notification.NotificationType.USER_KICK,
            user=friend,
            notification_user=user,
        )

        messages.success(
            request, f"You successfully removed {friend.username} from your friends!"
        )
        return redirect("friend_list")


class FriendBlockView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request: HttpRequest, pk: str) -> HttpResponseRedirect:
        user = cast(User, request.user)

        user_to_block = get_object_or_404(User, pk=pk)

        if user == user_to_block:
            messages.error(request, "You can't block yourself!")
            return redirect("friend_list")

        friendship = Friendship.objects.filter(
            Q(user=user, friend=user_to_block) | Q(user=user_to_block, friend=user)
        ).first()

        if not friendship:
            Friendship.objects.create(
                status=Friendship.FriendshipStatus.BLOCKED,
                user=user,
                friend=user_to_block,
                blocked_at=timezone.now(),
                blocked_by=user,
            )
        elif friendship.status == Friendship.FriendshipStatus.BLOCKED:
            messages.error(request, "You can't block this user!")
            return redirect("friend_list")
        else:
            friendship.status = Friendship.FriendshipStatus.BLOCKED
            friendship.blocked_at = timezone.now()
            friendship.blocked_by = user
            friendship.save()

        FriendRequest.objects.filter(
            Q(sender=user, receiver=user_to_block)
            | Q(sender=user_to_block, receiver=user),
            status=FriendRequest.RequestStatus.PENDING,
        ).update(status=FriendRequest.RequestStatus.DECLINED)

        Notification.objects.create(
            type=Notification.NotificationType.USER_BLOCK,
            user=user_to_block,
            notification_user=user,
        )

        messages.success(request, f"You successfully blocked {user_to_block.username}!")
        return redirect("friend_list")


class FriendRequestSentListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = "friendships/friend_request_sent_list.html"
    context_object_name = "requests_sent"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[FriendRequest]:
        user = cast(User, self.request.user)

        return (
            self.model.objects.filter(
                status=FriendRequest.RequestStatus.PENDING, sender=user
            )
            .select_related("receiver", "receiver__profile")
            .order_by("-sent_at")
        )


class FriendRequestCancelView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        user = cast(User, request.user)

        request_sent = get_object_or_404(
            FriendRequest,
            pk=pk,
            sender=user,
            status=FriendRequest.RequestStatus.PENDING,
        )
        request_sent.delete()

        Notification.objects.filter(
            type=Notification.NotificationType.FRIEND_REQUEST_RECEIVED,
            user=request_sent.receiver,
            notification_user=user,
            received_at=request_sent.sent_at,
        ).delete()

        messages.success(request, "You successfully cancelled request!")
        return redirect("friend_request_sent_list")


class FriendRequestReceivedListView(LoginRequiredMixin, ListView):
    model = FriendRequest
    template_name = "friendships/friend_request_received_list.html"
    context_object_name = "requests_received"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[FriendRequest]:
        user = cast(User, self.request.user)

        return (
            self.model.objects.filter(
                status=FriendRequest.RequestStatus.PENDING, receiver=user
            )
            .select_related("sender", "sender__profile")
            .order_by("-sent_at")
        )


class FriendAcceptRequestView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        user = cast(User, request.user)

        request_received = get_object_or_404(
            FriendRequest,
            pk=pk,
            receiver=user,
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

        Notification.objects.create(
            type=Notification.NotificationType.FRIEND_REQUEST_ACCEPTED,
            user=request_received.sender,
            notification_user=user,
        )

        messages.success(
            request, f"You are now friend with {request_received.sender.username}!"
        )
        return redirect("friend_request_received_list")


class FriendDeclineRequestView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        user = cast(User, request.user)

        request_received = get_object_or_404(
            FriendRequest,
            pk=pk,
            receiver=user,
            status=FriendRequest.RequestStatus.PENDING,
        )
        request_received.status = FriendRequest.RequestStatus.DECLINED
        request_received.save()

        Notification.objects.create(
            type=Notification.NotificationType.FRIEND_REQUEST_DECLINED,
            user=request_received.sender,
            notification_user=user,
        )

        messages.success(
            request, f"You declined request from {request_received.sender.username}!"
        )
        return redirect("friend_request_received_list")


class FriendBlockedListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_blocked_list.html"
    context_object_name = "friends_blocked"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[User]:
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
    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        user = cast(User, request.user)

        friend = get_object_or_404(User, pk=pk)
        friendship = Friendship.objects.filter(
            Q(user=user) & Q(friend=friend) & Q(blocked_by=user)
            | Q(user=friend) & Q(friend=user) & Q(blocked_by=user)
        ).first()

        if not friendship:
            messages.error(request, "You can't unblock this user!")
            return redirect("friend_blocked_list")

        friendship.delete()

        Notification.objects.create(
            type=Notification.NotificationType.USER_UNBLOCK,
            user=friend,
            notification_user=user,
        )

        messages.success(request, f"You successfully unblocked {friend.username}!")
        return redirect("friend_blocked_list")


class FriendBlockedByListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_blocked_by_list.html"
    context_object_name = "friends_blocked_by"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[User]:
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

    def get_queryset(self) -> QuerySet[User]:
        user = cast(User, self.request.user)

        queryset = (
            self.model.objects.exclude(pk=user.pk)
            .annotate(
                is_friend=Exists(
                    Friendship.objects.filter(
                        Q(status=Friendship.FriendshipStatus.ACTIVE),
                        Q(user=user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=user),
                    )
                ),
                request_sent_to=Exists(
                    FriendRequest.objects.filter(
                        status=FriendRequest.RequestStatus.PENDING,
                        sender=user,
                        receiver=OuterRef("pk"),
                    )
                ),
                request_sent_from=Exists(
                    FriendRequest.objects.filter(
                        status=FriendRequest.RequestStatus.PENDING,
                        sender=OuterRef("pk"),
                        receiver=user,
                    )
                ),
                blocked=Exists(
                    Friendship.objects.filter(
                        Q(blocked_by=user),
                        Q(user=user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=user),
                    )
                ),
                blocked_by=Exists(
                    Friendship.objects.filter(
                        Q(blocked_by=OuterRef("pk")),
                        Q(user=user, friend=OuterRef("pk"))
                        | Q(user=OuterRef("pk"), friend=user),
                    )
                ),
            )
            .distinct()
        )

        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(Q(username__icontains=search_query))

        return queryset


class FriendSendRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = FriendRequestForm
    model = FriendRequest
    template_name = "friendships/friend_send_request.html"

    def get_success_url(self) -> str:
        return reverse("friend_search")

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.friend = get_object_or_404(User, pk=kwargs.get("pk"))

    def test_func(self) -> bool:
        user = cast(User, self.request.user)

        is_user = user == self.friend

        has_friendship = Friendship.objects.filter(
            Q(
                status__in=[
                    Friendship.FriendshipStatus.BLOCKED,
                    Friendship.FriendshipStatus.ACTIVE,
                ]
            ),
            Q(user=user, friend=self.friend) | Q(user=self.friend, friend=user),
        ).exists()

        has_request = FriendRequest.objects.filter(
            Q(status=FriendRequest.RequestStatus.PENDING),
            Q(sender=user, receiver=self.friend) | Q(sender=self.friend, receiver=user),
        ).exists()

        return not (is_user or has_friendship or has_request)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, "You can't send request to this user!")
        return redirect("friend_search")

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["friend"] = self.friend
        return context

    def form_valid(self, form: FriendRequestForm) -> HttpResponse:
        user = cast(User, self.request.user)

        form.instance.status = FriendRequest.RequestStatus.PENDING
        form.instance.sender = user
        form.instance.receiver = self.friend

        Notification.objects.create(
            type=Notification.NotificationType.FRIEND_REQUEST_RECEIVED,
            user=self.friend,
            notification_user=user,
        )

        messages.success(
            self.request, f"Friend request sent to {self.friend.username}!"
        )

        return super().form_valid(form)
