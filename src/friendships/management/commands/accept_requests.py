from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone

from friendships.models import FriendRequest, Friendship


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Accepting request(s)...")

        self._accept_requests()

        self.stdout.write("Successfully accepted all requests!")

    @transaction.atomic
    def _accept_requests(self):
        requests = FriendRequest.objects.filter(
            status=FriendRequest.RequestStatus.PENDING
        ).update(status=FriendRequest.RequestStatus.ACCEPTED)

        for request in requests:
            friendship, created = Friendship.objects.get_or_create(
                user=request.sender,
                friend=request.receiver,
                defaults={"status": Friendship.FriendshipStatus.ACTIVE},
            )

            if not created:
                friendship.status = Friendship.FriendshipStatus.ACTIVE
                friendship.created_at = timezone.now()
                friendship.kicked_at = None
                friendship.blocked_at = None
                friendship.kicked_by = None
                friendship.blocked_by = None
                friendship.save()
