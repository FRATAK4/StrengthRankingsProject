from django.urls import path

from .views import (
    GroupDashboardView,
    GroupOwnedListView,
    GroupJoinedListView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView,
    GroupOwnedDetailView,
    GroupJoinedDetailView,
    GroupExitView,
    GroupSearchView,
    GroupSendRequestView,
    GroupRequestListView,
    GroupAcceptRequestView,
    GroupDeclineRequestView,
    GroupOwnedUserListView,
    GroupUserKickView,
    GroupUserBlockView,
    GroupOwnedRankingsView,
    GroupJoinedUserListView,
    GroupJoinedRankingsView,
)

urlpatterns = [
    path("", GroupDashboardView.as_view(), name="group_dashboard"),
    path("owned/", GroupOwnedListView.as_view(), name="group_owned_list"),
    path("owned/create/", GroupCreateView.as_view(), name="group_create"),
    path("owned/<int:pk>/", GroupOwnedDetailView.as_view(), name="group_owned_detail"),
    path("owned/<int:pk>/edit/", GroupUpdateView.as_view(), name="group_edit"),
    path("owned/<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    path(
        "owned/<int:pk>/users/",
        GroupOwnedUserListView.as_view(),
        name="group_owned_user_list",
    ),
    path(
        "owned/<int:pk>/users/<int:user_pk>/kick/",
        GroupUserKickView.as_view(),
        name="group_user_kick",
    ),
    path(
        "owned/<int:pk>/users/<int:user_pk>/block/",
        GroupUserBlockView.as_view(),
        name="group_user_block",
    ),
    path(
        "owned/<int:pk>/rankings/",
        GroupOwnedRankingsView.as_view(),
        name="group_owned_rankings",
    ),
    path(
        "owned/<int:pk>/requests/",
        GroupRequestListView.as_view(),
        name="group_request_list",
    ),
    path(
        "owned/<int:pk>/requests/<int:request_pk>/accept/",
        GroupAcceptRequestView.as_view(),
        name="group_request_accept",
    ),
    path(
        "owned/<int:pk>/requests/<int:request_pk>/decline/",
        GroupDeclineRequestView.as_view(),
        name="group_request_decline",
    ),
    path(
        "joined/", GroupJoinedListView.as_view(), name="group_joined_list"
    ),  # owned gruops, my gropu groups/joined?owned=true, ...
    path(
        "joined/<int:pk>/", GroupJoinedDetailView.as_view(), name="group_joined_detail"
    ),
    path("joined/<int:pk>/exit", GroupExitView.as_view(), name="group_exit"),
    path(
        "joined/<int:pk>/users/",
        GroupJoinedUserListView.as_view(),
        name="group_joined_user_list",
    ),
    path(
        "joined/<int:pk>/rankings/",
        GroupJoinedRankingsView.as_view(),
        name="group_joined_rankings",
    ),
    path("search/", GroupSearchView.as_view(), name="group_search"),
    path("search/<int:pk>/", GroupSendRequestView.as_view(), name="group_send_request"),
]
