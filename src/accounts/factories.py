import factory
from django.contrib.auth.models import User
from .models import Profile


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    image = factory.django.ImageField()
    gender = factory.Iterator(["male", "female"])
    age = factory.Faker("random_int", min=18, max=50)
    body_weight = factory.Faker(
        "pydecimal", left_digits=3, right_digits=1, min_value=50, max_value=120
    )


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttributeSequence(
        lambda obj, n: f"{obj.first_name}.{obj.last_name}{n}"
    )
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpass123")

    profile = factory.RelatedFactory(
        ProfileFactory,
        "user",
    )
