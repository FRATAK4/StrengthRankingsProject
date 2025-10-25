import random

import factory.django
from django.contrib.auth.models import User
from django.db.models import Q, OuterRef, Exists
from django.utils import timezone
from faker import Faker

from .models import Friendship, FriendRequest
from accounts.factories import UserFactory

from notifications.models import Notification

fake = Faker()


class FriendshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friendship

    status = factory.Iterator(["active", "kicked", "blocked"])

    @factory.lazy_attribute
    def created_at(self):
        match self.status:
            case "active":
                return timezone.now()
            case "kicked" | "blocked":
                return fake.date_between(start_date="-1m", end_date="today")

    @factory.lazy_attribute
    def kicked_at(self):
        match self.status:
            case "active":
                return None
            case "kicked":
                return timezone.now()
            case "blocked":
                return random.choice(
                    [
                        fake.date_between(start_date=self.created_at, end_date="today"),
                        None,
                    ]
                )

    @factory.lazy_attribute
    def blocked_at(self):
        match self.status:
            case "active" | "kicked":
                return None
            case "blocked":
                return timezone.now()

    user = factory.SubFactory(UserFactory)
    friend = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def kicked_by(self):
        if self.kicked_at:
            return random.choice([self.user, self.friend])
        return None

    @factory.lazy_attribute
    def blocked_by(self):
        if self.blocked_at:
            return random.choice([self.user, self.friend])
        return None


class FriendRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FriendRequest

    message = factory.Faker("text", max_nb_chars=500)
    status = factory.Iterator(["pending", "accepted", "declined"])

    @factory.lazy_attribute
    def sent_at(self):
        match self.status:
            case "pending":
                return timezone.now()
            case "accepted" | "declined":
                return fake.date_between(start_date="-1m", end_date="today")

    @factory.lazy_attribute
    def responded_at(self):
        match self.status:
            case "pending":
                return None
            case "accepted" | "declined":
                return timezone.now()

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)


class FriendSendRequestFactory(FriendRequestFactory):
    status = factory.Iterator("pending")
    sender = factory.Iterator(User.objects.all())  # type: ignore[assignment]

    @factory.lazy_attribute
    def receiver(self):
        has_friendship = Friendship.objects.filter(
            Q(
                status__in=[
                    Friendship.FriendshipStatus.BLOCKED,
                    Friendship.FriendshipStatus.ACTIVE,
                ]
            ),
            Q(user=self.sender, friend=OuterRef("pk"))
            | Q(user=OuterRef("pk"), friend=self.sender),
        )

        has_request = FriendRequest.objects.filter(
            Q(status=FriendRequest.RequestStatus.PENDING),
            Q(sender=self.sender, receiver=OuterRef("pk"))
            | Q(sender=OuterRef("pk"), receiver=self.sender),
        )

        users_to_send = (
            User.objects.exclude(
                pk=self.sender.pk,
            )
            .exclude(Exists(has_friendship))
            .exclude(Exists(has_request))
        )

        return random.choice(users_to_send)

    @factory.post_generation
    def create_notification(self, create, extracted, **kwargs):
        if not create:
            return

        Notification.objects.create(
            type=Notification.NotificationType.FRIEND_REQUEST_RECEIVED,
            user=self.receiver,
            notification_user=self.sender,
        )
