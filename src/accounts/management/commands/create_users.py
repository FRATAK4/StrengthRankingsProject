from django.core.management import BaseCommand

from accounts.factories import UserFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", type=int, default=1)

    def handle(self, *args, **options):
        count = options["count"]

        self.stdout.write(f"Creating {count} user(s)...")

        self._create_users(count)

        self.stdout.write(f"Successfully created {count} user(s)!")

    def _create_users(self, count):
        UserFactory.create_batch(count)
