from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Deleting all users..")

        self._delete_users()

        self.stdout.write("Successfully deleted all users!")

    def _delete_users(self) -> None:
        User.objects.filter(is_superuser=False).delete()
