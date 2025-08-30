from django.utils import timezone
import factory.django
from faker import Faker
import random

from .models import Group, GroupAddRequest, GroupMembership
from ..accounts.factories import UserFactory

fake = Faker()


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")
    description = factory.Faker("text", max_nb_chars=500)
    image = factory.django.ImageField()
    created_at = factory.LazyFunction(timezone.now)
    admin_user = factory.SubFactory(UserFactory)


class GroupAddRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupAddRequest

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

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)


class GroupMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GroupMembership

    status = factory.Iterator(["accepted", "kicked", "blocked"])

    @factory.lazy_attribute
    def started_at(self):
        match self.status:
            case "accepted":
                return timezone.now()
            case "kicked" | "blocked":
                return fake.date_between(start_date="-1m", end_date="today")

    @factory.lazy_attribute
    def kicked_at(self):
        match self.status:
            case "accepted":
                return None
            case "kicked":
                return timezone.now()
            case "blocked":
                return random.choice(
                    [
                        fake.date_between(start_date=self.started_at, end_date="today"),
                        None,
                    ]
                )

    @factory.lazy_attribute
    def blocked_at(self):
        match self.status:
            case "accepted" | "kicked":
                return None
            case "blocked":
                return timezone.now()

    user = factory.SubFactory(UserFactory)
    group = factory.SubFactory(GroupFactory)
