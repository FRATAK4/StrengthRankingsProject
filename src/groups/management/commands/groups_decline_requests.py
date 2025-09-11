from django.core.management import BaseCommand

from groups.models import GroupAddRequest, GroupMembership


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Declining request(s)...")

        self._decline_requests()

        self.stdout.write("Successfully declined all requests!")

    def _decline_requests(self):
        GroupAddRequest.objects.filter(
            status=GroupAddRequest.RequestStatus.PENDING
        ).update(status=GroupAddRequest.RequestStatus.DECLINED)
