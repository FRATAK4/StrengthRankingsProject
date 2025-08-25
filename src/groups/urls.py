from django.urls import path

from .views import (
    GroupDashboardView,
    GroupCreateView,
    GroupUpdateView,
    GroupDeleteView,
    GroupDetailView,
    GroupExitView,
    GroupSearchView,
    GroupSendRequestView,
    GroupRequestListView,
    GroupAcceptRequestView,
    GroupDeclineRequestView,
    GroupUserListView,
    GroupUserKickView,
    GroupUserBlockView,
    GroupRankingsView,
)

urlpatterns = [
    path("", GroupDashboardView.as_view(), name="group_dashboard"),
    path("create/", GroupCreateView.as_view(), name="group_create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("<int:pk>/edit/", GroupUpdateView.as_view(), name="group_edit"),
    path("<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
    path("<int:pk>/users/", GroupUserListView.as_view(), name="group_user_list"),
    path(
        "<int:pk>/users/<int:user_pk>/kick/",
        GroupUserKickView.as_view(),
        name="group_user_kick",
    ),
    path(
        "<int:pk>/users/<int:user_pk>/block/",
        GroupUserBlockView.as_view(),
        name="group_user_block",
    ),
    path(
        "<int:pk>/rankings/",
        GroupRankingsView.as_view(),
        name="group_rankings",
    ),
    path(
        "<int:pk>/requests/",
        GroupRequestListView.as_view(),
        name="group_request_list",
    ),
    path(
        "<int:pk>/requests/<int:request_pk>/accept/",
        GroupAcceptRequestView.as_view(),
        name="group_request_accept",
    ),
    path(
        "<int:pk>/requests/<int:request_pk>/decline/",
        GroupDeclineRequestView.as_view(),
        name="group_request_decline",
    ),
    path("<int:pk>/exit/", GroupExitView.as_view(), name="group_exit"),
    path("search/", GroupSearchView.as_view(), name="group_search"),
    path("search/<int:pk>/", GroupSendRequestView.as_view(), name="group_send_request"),
]
