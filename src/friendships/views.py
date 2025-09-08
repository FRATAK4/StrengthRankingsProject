from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Exists, Q, OuterRef
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
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
            Q(sent_friendships__friend=self.request.user)
            & Q(sent_friendships__status=Friendship.FriendshipStatus.ACTIVE)
            | Q(received_friendships__user=self.request.user)
            & Q(received_friendships__status=Friendship.FriendshipStatus.ACTIVE)
        )


class FriendSearchView(LoginRequiredMixin, ListView):
    model = User
    template_name = "friendships/friend_search.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        return self.model.objects.exclude(pk=self.request.user.pk).annotate(
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
                    status=Friendship.FriendshipStatus.BLOCKED,
                    user=self.request.user,
                    friend=OuterRef("pk"),
                )
            ),
            blocked_by=Exists(
                Friendship.objects.filter(
                    status=Friendship.FriendshipStatus.BLOCKED,
                    user=OuterRef("pk"),
                    friend=self.request.user,
                )
            ),
        )


class FriendSendRequestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = FriendRequestForm
    model = FriendRequest
    template_name = "friendships/friend_send_request.html"

    def get_success_url(self):
        return reverse_lazy("")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.friend = get_object_or_404(User, pk=kwargs.get("pk"))

    def test_func(self):
        return not Exists(
            Friendship.objects.filter(
                Q(status=Friendship.FriendshipStatus.BLOCKED)
                | Q(status=Friendship.FriendshipStatus.ACTIVE),
                Q(user=self.request.user, friend=self.friend)
                | Q(user=self.friend, friend=self.request.user),
            )
        ) and not Exists(
            FriendRequest.objects.filter(
                Q(status=FriendRequest.RequestStatus.PENDING),
                Q(sender=self.request.user, receiver=self.friend)
                | Q(sender=self.friend, receiver=self.request.user),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["friend"] = self.friend
        return context

    def form_valid(self, form):
        form.instance.status = FriendRequest.RequestStatus.PENDING
        form.instance.sender = self.request.user
        form.instance.receiver = self.friend

        return super().form_valid(form)
