from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView
from typing import cast
from django.contrib.auth.models import User

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Notification]:
        user = cast(User, self.request.user)

        return self.model.objects.filter(user=user).select_related(
            "notification_user", "notification_group"
        )
