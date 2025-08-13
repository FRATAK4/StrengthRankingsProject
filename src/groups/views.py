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


class OwnedGroupListView(ListView):
    pass


class JoinedGroupListView(ListView):
    pass


class GroupCreateView(CreateView):
    pass


class GroupDetailView(DetailView):
    pass


class GroupUpdateView(UpdateView):
    pass


class GroupDeleteView(DeleteView):
    pass


class GroupSearchView(View):
    pass
