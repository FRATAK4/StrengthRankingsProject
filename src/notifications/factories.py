import factory.django
from django.utils import timezone

from .models import Notification
from accounts.factories import UserFactory
from groups.factories import GroupFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    type = factory.Iterator(Notification.NotificationType.choices)
    received_at = factory.lazy_attribute(lambda: timezone.now)
    is_read = False
    user = factory.SubFactory(UserFactory)

    notification_user = factory.SubFactory(UserFactory)
    notification_group = factory.SubFactory(GroupFactory)
