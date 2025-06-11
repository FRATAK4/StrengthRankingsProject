from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    class Genders(models.TextChoices):
        MALE = "male"
        FEMALE = "female"

    nick = models.CharField(max_length=50)
    image = models.ImageField(
        default="profile_pics/default.jpg", upload_to="profile_pics"
    )
    gender = models.CharField(max_length=30, choices=Genders.choices)
    age = models.IntegerField()
    bodyweight = models.DecimalField(max_digits=4, decimal_places=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
