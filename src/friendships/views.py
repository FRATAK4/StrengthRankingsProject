from django.shortcuts import render
from django.views.generic import ListView

from .models import Friendship, FriendRequest


class FriendListView(ListView):
    model = Friendship
    template_name = "friendships/friend_list.html"


class FriendRequestListView(ListView):
    model = FriendRequest
    template_name = "friendships/friend_request_list.html"
