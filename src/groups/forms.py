from django.forms import ModelForm
from .models import Group, GroupAddRequest


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ["name", "description", "image"]


class GroupAddRequestForm(ModelForm):
    class Meta:
        model = GroupAddRequest
        fields = ["message"]
