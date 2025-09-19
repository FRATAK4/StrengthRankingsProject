from django.db import models
from django.contrib.auth.models import User


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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications_received"
    )

    notification_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_notifications_sent"
    )
    notification_group = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="group_notifications_sent"
    )

    @property
    def message(self):
        match self.type:
            case "friend_request_received":
                return f"{self.notification_user} has sent you a friendship request"
            case "friend_request_accepted":
                return f"{self.notification_user} has accepted your friendship request"
            case "friend_request_decline":
                return f"{self.notification_user} has declined your friendship request"
            case "user_kick":
                return f"{self.notification_user} has kicked you from friends"
            case "user_block":
                return f"{self.notification_user} has blocked you"
            case "user_unblock":
                return f"{self.notification_user} has unblocked you"
            case "group_request_received":
                return f"{self.notification_user} wants to join to your {self.notification_group} group"
            case "group_request_accepted":
                return f"{self.notification_user} has accepted your request to join {self.notification_group} group"
            case "group_request_decline":
                return f"{self.notification_user} has declined your request to join {self.notification_group} group"
            case "group_kick":
                return f"{self.notification_user} has kicked you from {self.notification_group} group"
            case "group_block":
                return f"{self.notification_user} has blocked you from {self.notification_group} group"
            case "group_unblock":
                return f"{self.notification_user} has unblocked you from {self.notification_group} group"
        return None

    @property
    def url(self):
        match self.type:
            case "friend_request_received":
                return f"{{% url 'friend_request_received_list' %}}"
            case "group_request_received":
                return (
                    f"{{% url 'group_request_list' pk={self.notification_group.pk} %}}"
                )
            case "group_request_accepted":
                return f"{{% url 'group_detail' pk={self.notification_group.pk} %}}"
        return None
