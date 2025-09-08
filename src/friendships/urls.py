from django.urls import path

from .views import (
    FriendSearchView,
    FriendSendRequestView,
    FriendDashboardView,
    FriendListView,
    FriendRequestSentListView,
)

urlpatterns = [
    path("/", FriendDashboardView.as_view(), name="friend_dashboard"),
    path("list/", FriendListView.as_view(), name="friend_list"),
    path(
        "request_sent/",
        FriendRequestSentListView.as_view(),
        name="friend_request_sent_list",
    ),
    path("search/", FriendSearchView.as_view(), name="friend_search"),
    path(
        "search/<int:pk>", FriendSendRequestView.as_view(), name="friend_send_request"
    ),
]
