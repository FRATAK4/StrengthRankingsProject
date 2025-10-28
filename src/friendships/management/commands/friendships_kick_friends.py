import random
from typing import Any

from django.core.management import BaseCommand
from django.db import transaction
from django.utils import timezone

from friendships.models import Friendship

from notifications.models import Notification


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Kicking friend(s)...")

        self._kick_friends()

        self.stdout.write("Successfully kicked all friends!")

    @transaction.atomic
    def _kick_friends(self) -> None:
        friendships = Friendship.objects.filter(
            status=Friendship.FriendshipStatus.ACTIVE
        )
        for friendship in friendships:
            friendship.status = Friendship.FriendshipStatus.KICKED
            friendship.kicked_at = timezone.now()
            friendship.kicked_by = random.choice([friendship.user, friendship.friend])
            friendship.save()

            Notification.objects.create(
                type=Notification.NotificationType.USER_KICK,
                user=(
                    friendship.user
                    if friendship.kicked_by == friendship.friend
                    else friendship.friend
                ),
                notification_user=friendship.kicked_by,
            )
