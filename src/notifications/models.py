from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from groups.models import Group


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
    def message(self):
        match self.type:
            case self.NotificationType.FRIEND_REQUEST_RECEIVED:
                return f"{self.notification_user} has sent you a friendship request"
            case self.NotificationType.FRIEND_REQUEST_ACCEPTED:
                return f"{self.notification_user} has accepted your friendship request"
            case self.NotificationType.FRIEND_REQUEST_DECLINED:
                return f"{self.notification_user} has declined your friendship request"
            case self.NotificationType.USER_KICK:
                return f"{self.notification_user} has kicked you from friends"
            case self.NotificationType.USER_BLOCK:
                return f"{self.notification_user} has blocked you"
            case self.NotificationType.USER_UNBLOCK:
                return f"{self.notification_user} has unblocked you"
            case self.NotificationType.GROUP_REQUEST_RECEIVED:
                return f"{self.notification_user} wants to join to your {self.notification_group} group"
            case self.NotificationType.GROUP_REQUEST_ACCEPTED:
                return f"{self.notification_user} has accepted your request to join {self.notification_group} group"
            case self.NotificationType.GROUP_REQUEST_DECLINED:
                return f"{self.notification_user} has declined your request to join {self.notification_group} group"
            case self.NotificationType.GROUP_KICK:
                return f"{self.notification_user} has kicked you from {self.notification_group} group"
            case self.NotificationType.GROUP_BLOCK:
                return f"{self.notification_user} has blocked you from {self.notification_group} group"
            case self.NotificationType.GROUP_UNBLOCK:
                return f"{self.notification_user} has unblocked you from {self.notification_group} group"
        return "Notification"

    @property
    def url(self):
        match self.type:
            case self.NotificationType.FRIEND_REQUEST_RECEIVED:
                return reverse("friend_request_received_list")
            case self.NotificationType.GROUP_REQUEST_RECEIVED:
                return reverse(
                    "group_request_list", kwargs={"pk": self.notification_group.pk}
                )
            case self.NotificationType.GROUP_REQUEST_ACCEPTED:
                return reverse(
                    "group_detail", kwargs={"pk": self.notification_group.pk}
                )
        return None
