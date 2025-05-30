from django.db import models

class Profile(models.Model):
    class Genders(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'

    nick = models.CharField(max_length=50)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    gender = models.CharField(max_length=30, choices=Genders.choices)
    age = models.IntegerField()
    bodyweight = models.DecimalField(decimal_places=1)
