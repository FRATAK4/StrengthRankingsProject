from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView, TemplateView,
)


class GroupDashboardView(TemplateView):
    template_name = "groups/group_dashboard.html"


class GroupListView(ListView):
    pass


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
