from django.core.management import BaseCommand
from argparse import ArgumentParser
from accounts.factories import UserFactory


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("count", type=int, default=1)

    def handle(self, *args: int, **options: int) -> None:
        count = options["count"]

        self.stdout.write(f"Creating {count} user(s)...")

        self._create_users(count)

        self.stdout.write(f"Successfully created {count} user(s)!")

    def _create_users(self, count: int) -> None:
        UserFactory.create_batch(count)
