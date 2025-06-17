from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Group, GroupMembership, GroupAddRequest


class GroupDetailView(DetailView):
    model = Group
    template_name = "groups/group.html"


class GroupRankingDetailView(DetailView):
    model = Group
    template_name = "groups/group_ranking.html"


class GroupListView(ListView):
    model = Group
    template_name = "groups/group_list.html"


class UserGroupListView(ListView):
    model = GroupMembership
    template_name = "groups/user_group_list.html"


class GroupRequestListView(ListView):
    model = GroupAddRequest
    template_name = "groups/group_request_list.html"
