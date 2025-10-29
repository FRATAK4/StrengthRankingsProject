from typing import Any
from django.core.management import BaseCommand
from groups.models import Group


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        nb_groups = self._count_groups()

        self.stdout.write(f"There is {nb_groups} groups created")

    def _count_groups(self) -> int:
        return Group.objects.all().count()
