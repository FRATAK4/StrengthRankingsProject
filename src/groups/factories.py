from django.utils import timezone
import factory.django

from .models import Group
from ..accounts.factories import UserFactory


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")
    description = factory.Faker("text", max_nb_chars=500)
    image = factory.django.ImageField()
    created_at = factory.LazyFunction(timezone.now)
    admin_user = factory.SubFactory(UserFactory)
