from django.urls import path

from .views import (
    GroupDashboardView,
    GroupOwnedListView,
    GroupJoinedListView,
    GroupCreateView,
    GroupDetailView,
    GroupUpdateView,
    GroupDeleteView,
)

urlpatterns = [
    path("", GroupDashboardView.as_view(), name="group_dashboard"),
    path("owned/", GroupOwnedListView.as_view(), name="group_owned_list"),
    path("joined/", GroupJoinedListView.as_view(), name="group_joined_list"),
    path("create/", GroupCreateView.as_view(), name="group_create"),
    path("<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("<int:pk>/edit/", GroupUpdateView.as_view(), name="group_edit"),
    path("<int:pk>/delete/", GroupDeleteView.as_view(), name="group_delete"),
]
