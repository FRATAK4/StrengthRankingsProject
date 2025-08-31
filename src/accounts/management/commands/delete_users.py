from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f"Deleting all users..")

        self._delete_users()

        self.stdout.write(f"Successfully deleted all users!")

    def _delete_users(self):
        User.objects.filter(is_superuser=False).delete()
