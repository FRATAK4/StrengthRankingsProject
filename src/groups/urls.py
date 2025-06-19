from django.urls import path

from .views import (
    GroupListView,
    UserGroupListView,
    GroupRequestListView,
    GroupDetailView,
    GroupRankingDetailView,
    GroupCreateView,
)

urlpatterns = [
    path("", GroupListView.as_view(), name="groups"),
    path("user/", UserGroupListView.as_view(), name="groups-user"),
    path("create/", GroupCreateView.as_view(), name="groups-create"),
    path("requests/", GroupRequestListView.as_view(), name="groups-requests"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group"),
    path("<int:pk>/rankings/", GroupRankingDetailView.as_view(), name="group-ranking"),
]
