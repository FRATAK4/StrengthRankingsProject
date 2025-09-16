import random

from django.core.management import BaseCommand
from django.db.models import F
from django.utils import timezone

from friendships.models import Friendship


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Kicking friend(s)...")

        self._kick_friends()

        self.stdout.write("Successfully kicked all friends!")

    def _kick_friends(self):
        friendships = Friendship.objects.filter(
            status=Friendship.FriendshipStatus.ACTIVE
        )
        for friendship in friendships:
            friendship.status = Friendship.FriendshipStatus.KICKED
            friendship.kicked_at = timezone.now()
            friendship.kicked_by = random.choice([friendship.user, friendship.friend])
            friendship.save()
