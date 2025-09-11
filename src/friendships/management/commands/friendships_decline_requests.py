from django.core.management import BaseCommand

from friendships.models import FriendRequest


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Declining request(s)...")

        self._decline_requests()

        self.stdout.write("Successfully declined all requests!")

    def _decline_requests(self):
        FriendRequest.objects.filter(status=FriendRequest.RequestStatus.PENDING).update(
            status=FriendRequest.RequestStatus.DECLINED
        )
