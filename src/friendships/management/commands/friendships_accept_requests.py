from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from friendships.models import FriendRequest, Friendship


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Accepting request(s)...")

        self._accept_requests()

        self.stdout.write("Successfully accepted all requests!")

    @transaction.atomic
    def _accept_requests(self):
        requests = list(
            FriendRequest.objects.filter(status=FriendRequest.RequestStatus.PENDING)
        )

        FriendRequest.objects.filter(status=FriendRequest.RequestStatus.PENDING).update(
            status=FriendRequest.RequestStatus.ACCEPTED
        )

        for request in requests:
            friendship = Friendship.objects.filter(
                Q(user=request.sender, friend=request.receiver)
                | Q(user=request.receiver, friend=request.sender),
                status=Friendship.FriendshipStatus.KICKED,
            ).first()

            if not friendship:
                Friendship.objects.create(
                    status=Friendship.FriendshipStatus.ACTIVE,
                    user=request.sender,
                    friend=request.receiver,
                )
            else:
                friendship.status = Friendship.FriendshipStatus.ACTIVE
                friendship.created_at = timezone.now()
                friendship.kicked_at = None
                friendship.blocked_at = None
                friendship.user = request.sender
                friendship.friend = request.receiver
                friendship.kicked_by = None
                friendship.blocked_by = None
                friendship.save()
