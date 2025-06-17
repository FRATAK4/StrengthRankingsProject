from django.urls import path

from src.friendships.views import FriendListView, FriendRequestListView

urlpatterns = [
    path("", FriendListView.as_view(), name="friendships"),
    path("requests/", FriendRequestListView.as_view(), name="friendships-requests"),
]
