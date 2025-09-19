import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from friendships.models import Friendship

from notifications.models import Notification


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", type=int, default=1)

    def handle(self, *args, **options):
        count = options["count"]
        users = User.objects.select_related("profile")

        self.stdout.write(f"Blocking {count} user(s) for each user...")

        for user in users:
            nb_blocked_users = self._block_users(count, user)
            self.stdout.write(
                f"Successfully blocked {nb_blocked_users} user(s) from {user.username}"
            )

        self.stdout.write(f"Successfully blocked user(s)!")

    @transaction.atomic
    def _block_users(self, count, user):
        available_users = list(
            User.objects.exclude(
                Q(
                    sent_friendships__friend=user,
                    sent_friendships__status=Friendship.FriendshipStatus.BLOCKED,
                )
                | Q(
                    accepted_friendships__user=user,
                    accepted_friendships__status=Friendship.FriendshipStatus.BLOCKED,
                )
                | Q(pk=user.pk)
            )
        )

        users_to_block = random.sample(
            available_users, min(count, len(available_users))
        )

        for user_to_block in users_to_block:
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
            else:
                friendship.status = Friendship.FriendshipStatus.BLOCKED
                friendship.blocked_at = timezone.now()
                friendship.blocked_by = user
                friendship.save()

            Notification.objects.create(
                type=Notification.NotificationType.USER_BLOCK,
                user=user_to_block,
                notification_user=user,
            )

        return len(users_to_block)
