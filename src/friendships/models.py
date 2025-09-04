from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    class FriendshipStatus(models.TextChoices):
        ACTIVE = "accepted"
        KICKED = "kicked"
        BLOCKED = "blocked"

    status = models.CharField(max_length=30, choices=FriendshipStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    kicked_at = models.DateTimeField(null=True)
    blocked_at = models.DateTimeField(null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_friendships"
    )
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accepted_friendships"
    )
    kicked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="kicked_friendships", null=True
    )
    blocked_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocked_friendships", null=True
    )

    class Meta:
        unique_together = (("user", "friend"),)


class FriendRequest(models.Model):
    class RequestStatus(models.TextChoices):
        PENDING = "pending"
        ACCEPTED = "accepted"
        DECLINED = "declined"

    message = models.TextField()
    status = models.CharField(max_length=30, choices=RequestStatus.choices)
    sent_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_friend_requests"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_friend_requests"
    )

    class Meta:
        unique_together = (("sender", "receiver"),)
