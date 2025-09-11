from django.core.management import BaseCommand
from django.db.models import F
from django.utils import timezone

from groups.models import GroupMembership


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Kicking user(s)...")

        self._kick_users()

        self.stdout.write("Successfully kicked all users!")

    def _kick_users(self):
        GroupMembership.objects.filter(
            status=GroupMembership.MembershipStatus.ACCEPTED
        ).exclude(user=F("group__admin_user")).update(
            status=GroupMembership.MembershipStatus.KICKED, kicked_at=timezone.now()
        )
