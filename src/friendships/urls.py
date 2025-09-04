from django.urls import path

from .views import FriendSearchView, FriendSendRequestView

urlpatterns = [
    path("search/", FriendSearchView.as_view(), name="friend_search"),
    path(
        "search/<int:pk>", FriendSendRequestView.as_view(), name="friend_send_request"
    ),
]
