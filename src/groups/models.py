from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000)
    image = models.ImageField(default='group_pics/default.jpg', upload_to='group_pics')
    members = models.ManyToManyField(User)
    join_requests = models.ManyToManyField(User)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
