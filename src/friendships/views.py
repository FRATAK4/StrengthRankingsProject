from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, Q, OuterRef
from django.views.generic import ListView

from django.contrib.auth.models import User
from .models import Friendship, FriendRequest


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
