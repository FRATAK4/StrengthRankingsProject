from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


class GroupDashboardView(View):
    pass


class GroupOwnedListView(ListView):
    pass


class GroupCreateView(CreateView):
    pass


class GroupOwnedDetailView(DetailView):
    pass


class GroupUpdateView(UpdateView):
    pass


class GroupDeleteView(DeleteView):
    pass


class GroupOwnedUserListView(ListView):
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


class GroupOwnedRankingsView(ListView):
    pass


class GroupJoinedListView(ListView):
    pass


class GroupJoinedDetailView(DetailView):
    pass


class GroupExitView(DeleteView):
    pass


class GroupJoinedUserListView(ListView):
    pass


class GroupJoinedRankingsView(ListView):
    pass


class GroupSearchView(ListView):
    pass


class GroupSendRequestView(View):
    pass
