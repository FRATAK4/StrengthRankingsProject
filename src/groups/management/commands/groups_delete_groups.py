from django.core.management import BaseCommand
from groups.models import Group


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Deleting all groups...")

        self._delete_groups()

        self.stdout.write("Successfully deleted all groups!")

    def _delete_groups(self):
        Group.objects.all().delete()
