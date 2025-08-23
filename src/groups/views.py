from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import Group


class GroupDashboardView(View):
    def get(self):
        groups_hosted = self.request.user.groups_hosted.all()
        groups_joined = self.request.user.group_memberships.values_list("group", flat=True)
        context = {
            "groups_hosted": groups_hosted,
            "groups_joined": groups_joined,
        }
        return render(self.request, "group_dashboard.html", context=context)

class GroupCreateView(CreateView):
    pass


class GroupDetailView(DetailView):
    pass


class GroupUpdateView(UpdateView):
    pass


class GroupDeleteView(DeleteView):
    pass


class GroupUserKickView(View):
    pass


class GroupUserBlockView(View):
    pass


class GroupRequestListView(ListView):
    pass


class GroupAcceptRequestView(View):
    pass


class GroupDeclineRequestView(View):
    pass


class GroupRankingsView(ListView):
    pass


class GroupUserListView(ListView):
    pass


class GroupExitView(DeleteView):
    pass


class GroupSearchView(ListView):
    pass


class GroupSendRequestView(View):
    pass
