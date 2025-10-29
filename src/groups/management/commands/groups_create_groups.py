from argparse import ArgumentParser
from typing import Any

from django.core.management import BaseCommand

from groups.factories import GroupFactoryExistingAdmin


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("count", type=int, default=1)

    def handle(self, *args: Any, **options: Any) -> None:
        count = options["count"]

        self.stdout.write(f"Creating {count} group(s)...")

        self._create_groups(count)

        self.stdout.write(f"Successfully created {count} group(s)!")

    def _create_groups(self, count: int) -> None:
        GroupFactoryExistingAdmin.create_batch(count)
