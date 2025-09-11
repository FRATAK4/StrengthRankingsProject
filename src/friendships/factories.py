import random

import factory.django
from django.utils import timezone
from faker import Faker

from .models import Friendship
from accounts.factories import UserFactory

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
