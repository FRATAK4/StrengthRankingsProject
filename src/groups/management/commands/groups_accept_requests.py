from typing import Any

from django.core.management import BaseCommand
from django.db import transaction

from groups.models import GroupAddRequest, GroupMembership


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> None:
        self.stdout.write("Accepting request(s)...")

        self._accept_requests()

        self.stdout.write("Successfully accepted all requests!")

    @transaction.atomic
    def _accept_requests(self) -> None:
        join_requests = GroupAddRequest.objects.filter(
            status=GroupAddRequest.RequestStatus.PENDING
        )

        for join_request in join_requests:
            join_request.status = GroupAddRequest.RequestStatus.ACCEPTED
            join_request.save()

            membership, created = GroupMembership.objects.get_or_create(
                user=join_request.user,
                group=join_request.group,
                defaults={"status": GroupMembership.MembershipStatus.ACCEPTED},
            )
            if not created:
                membership.status = GroupMembership.MembershipStatus.ACCEPTED
                membership.kicked_at = None
                membership.blocked_at = None
                membership.save()
