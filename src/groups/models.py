from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(default="group_pics/default.jpg", upload_to="group_pics")
    admin_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="groups_hosted"
    )


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
        unique_together = (("user", "group"),)


class GroupMembership(models.Model):
    class MembershipStatus(models.TextChoices):
        ACCEPTED = "accepted"
        KICKED = "kicked"
        BLOCKED = "blocked"

    status = models.CharField(max_length=30, choices=MembershipStatus.choices)
    started_at = models.DateTimeField(auto_now_add=True)
    kicked_at = models.DateTimeField()
    blocked_at = models.DateTimeField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_memberships"
    )
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="user_memberships"
    )

    class Meta:
        unique_together = (("user", "group"),)
