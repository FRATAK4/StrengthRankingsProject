from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from groups.models import Group
from typing import cast


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        FRIEND_REQUEST_RECEIVED = "friend_request_received"
        FRIEND_REQUEST_ACCEPTED = "friend_request_accepted"
        FRIEND_REQUEST_DECLINED = "friend_request_declined"
        USER_KICK = "user_kick"
        USER_BLOCK = "user_block"
        USER_UNBLOCK = "user_unblock"
        GROUP_REQUEST_RECEIVED = "group_request_received"
        GROUP_REQUEST_ACCEPTED = "group_request_accepted"
        GROUP_REQUEST_DECLINED = "group_request_declined"
        GROUP_KICK = "group_kick"
        GROUP_BLOCK = "group_block"
        GROUP_UNBLOCK = "group_unblock"

    type = models.CharField(max_length=30, choices=NotificationType.choices)
    received_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications_received"
    )

    notification_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_notifications_sent",
        null=True,
    )
    notification_group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="group_notifications_sent",
        null=True,
    )

    class Meta:
        ordering = ["-received_at"]

    @property
    def message(self) -> str:
        notification_user = cast(User, self.notification_user)
        notification_group = cast(Group, self.notification_group)

        match self.type:
            case self.NotificationType.FRIEND_REQUEST_RECEIVED:
                return f"{notification_user} has sent you a friendship request"
            case self.NotificationType.FRIEND_REQUEST_ACCEPTED:
                return f"{notification_user} has accepted your friendship request"
            case self.NotificationType.FRIEND_REQUEST_DECLINED:
                return f"{notification_user} has declined your friendship request"
            case self.NotificationType.USER_KICK:
                return f"{notification_user} has kicked you from friends"
            case self.NotificationType.USER_BLOCK:
                return f"{notification_user} has blocked you"
            case self.NotificationType.USER_UNBLOCK:
                return f"{notification_user} has unblocked you"
            case self.NotificationType.GROUP_REQUEST_RECEIVED:
                return f"{notification_user} wants to join to your {notification_group} group"
            case self.NotificationType.GROUP_REQUEST_ACCEPTED:
                return f"{notification_user} has accepted your request to join {notification_group} group"
            case self.NotificationType.GROUP_REQUEST_DECLINED:
                return f"{notification_user} has declined your request to join {notification_group} group"
            case self.NotificationType.GROUP_KICK:
                return f"{notification_user} has kicked you from {notification_group} group"
            case self.NotificationType.GROUP_BLOCK:
                return f"{notification_user} has blocked you from {notification_group} group"
            case self.NotificationType.GROUP_UNBLOCK:
                return f"{notification_user} has unblocked you from {notification_group} group"
        return "Notification"

    @property
    def url(self) -> str | None:
        notification_group = cast(Group, self.notification_group)

        match self.type:
            case self.NotificationType.FRIEND_REQUEST_RECEIVED:
                return reverse("friend_request_received_list")
            case self.NotificationType.GROUP_REQUEST_RECEIVED:
                return reverse(
                    "group_request_list", kwargs={"pk": notification_group.pk}
                )
            case self.NotificationType.GROUP_REQUEST_ACCEPTED:
                return reverse("group_detail", kwargs={"pk": notification_group.pk})
        return None
