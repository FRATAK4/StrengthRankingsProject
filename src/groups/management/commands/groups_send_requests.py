from argparse import ArgumentParser
from typing import Any

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from groups.factories import GroupSendRequestFactory


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument("count", type=int, default=1)

    def handle(self, *args: Any, **options: Any) -> None:
        count = options["count"]
        users = User.objects.all()

        self.stdout.write(f"Sending {count} request(s) from each user...")

        for user in users:
            self._send_requests(count, user)

        self.stdout.write(f"Successfully sent {count} request(s) from each user!")

    def _send_requests(self, count: int, user: User) -> None:
        GroupSendRequestFactory.create_batch(count, user=user)
