from typing import Any

from django.core.management import BaseCommand
from django.db import transaction

from friendships.models import FriendRequest

from notifications.models import Notification


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Declining request(s)...")

        self._decline_requests()

        self.stdout.write("Successfully declined all requests!")

    @transaction.atomic
    def _decline_requests(self) -> None:
        requests = list(
            FriendRequest.objects.filter(status=FriendRequest.RequestStatus.PENDING)
        )

        FriendRequest.objects.filter(status=FriendRequest.RequestStatus.PENDING).update(
            status=FriendRequest.RequestStatus.DECLINED
        )

        for request in requests:
            Notification.objects.create(
                type=Notification.NotificationType.FRIEND_REQUEST_DECLINED,
                user=request.sender,
                notification_user=request.receiver,
            )
