from __future__ import annotations

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Q, QuerySet


class GroupManager(models.Manager):
    def with_member_count(self) -> QuerySet[Group]:
        return self.get_queryset().annotate(  # type: ignore[no-any-return]
            member_count=Count(
                "user_memberships",
                filter=Q(
                    user_memberships__status=GroupMembership.MembershipStatus.ACCEPTED
                ),
            )
        )


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(default="group_pics/default.jpg", upload_to="group_pics")
    created_at = models.DateTimeField(auto_now_add=True)
    admin_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="groups_hosted"
    )
    objects = GroupManager()

    def __str__(self) -> str:
        return f"{self.name}"


class GroupAddRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        DECLINED = "declined"

    message = models.TextField()
    status = models.CharField(max_length=30, choices=RequestStatus.choices)
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_add_requests"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="user_add_requests"
    )

    class Meta:
        unique_together = (("user", "group", "status", "sent_at", "responded_at"),)


class GroupMembership(models.Model):
    class MembershipStatus(models.TextChoices):
        ACCEPTED = "accepted"
        KICKED = "kicked"
        BLOCKED = "blocked"

    status = models.CharField(max_length=30, choices=MembershipStatus.choices)
    started_at = models.DateTimeField(auto_now_add=True)
    kicked_at = models.DateTimeField(null=True)
    blocked_at = models.DateTimeField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_memberships"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="user_memberships"
    )

    class Meta:
        unique_together = (("user", "group"),)
