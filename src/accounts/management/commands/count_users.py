from typing import Any
from django.core.management import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        nb_users = self._count_users()

        self.stdout.write(f"There is {nb_users} users created")

    def _count_users(self) -> int:
        return User.objects.all().count()
