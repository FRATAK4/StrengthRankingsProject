from django.urls import path

from .views import (
    FriendSearchView,
    FriendSendRequestView,
    FriendDashboardView,
    FriendListView,
    FriendRequestSentListView,
    FriendRequestReceivedListView,
    FriendKickView,
    FriendBlockView,
    FriendAcceptRequestView,
    FriendDeclineRequestView,
    FriendBlockedListView,
    FriendUnblockView,
    FriendBlockedByListView,
)

urlpatterns = [
    path("/", FriendDashboardView.as_view(), name="friend_dashboard"),
    path("list/", FriendListView.as_view(), name="friend_list"),
    path("list/<int:pk>/kick/", FriendKickView.as_view(), name="friend_kick"),
    path("list/<int:pk>/block/", FriendBlockView.as_view(), name="friend_block"),
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
    path(
        "request_received/<int:pk>/accept/",
        FriendAcceptRequestView.as_view(),
        name="friend_request_accept",
    ),
    path(
        "request_received/<int:pk>/decline/",
        FriendDeclineRequestView.as_view(),
        name="friend_request_decline",
    ),
    path("blocked/", FriendBlockedListView.as_view(), name="friend_blocked_list"),
    path(
        "blocked/<int:pk>/unblock/", FriendUnblockView.as_view(), name="friend_unblock"
    ),
    path(
        "blocked_by/", FriendBlockedByListView.as_view(), name="friend_blocked_by_list"
    ),
    path("search/", FriendSearchView.as_view(), name="friend_search"),
    path(
        "search/<int:pk>", FriendSendRequestView.as_view(), name="friend_send_request"
    ),
]
