from django.forms import ModelForm

from .models import FriendRequest


class FriendRequestForm(ModelForm):
    class Meta:
        model = FriendRequest
        fields = ["message"]
