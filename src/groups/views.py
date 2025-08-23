from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .forms import GroupForm
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
    form_class = GroupForm
    template_name = "groups/group_create.html"

    def get_success_url(self):
        return reverse("group_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        group = form.save(commit=False)
        group.admin_user = self.request.user
        group.save()
        return super().form_valid(form)

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
