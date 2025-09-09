from django.urls import path

from .views import (
    FriendSearchView,
    FriendSendRequestView,
    FriendDashboardView,
    FriendListView,
    FriendRequestSentListView,
    FriendRequestReceivedListView,
    FriendKickView,
)

urlpatterns = [
    path("/", FriendDashboardView.as_view(), name="friend_dashboard"),
    path("list/", FriendListView.as_view(), name="friend_list"),
    path("list/<int:pk>/kick/", FriendKickView.as_view(), name="friend_kick"),
    path(
        "request_sent/",
        FriendRequestSentListView.as_view(),
        name="friend_request_sent_list",
    ),
    path(
        "request_received/",
        FriendRequestReceivedListView.as_view(),
        name="friend_request_received_list",
    ),
    path("search/", FriendSearchView.as_view(), name="friend_search"),
    path(
        "search/<int:pk>", FriendSendRequestView.as_view(), name="friend_send_request"
    ),
]
