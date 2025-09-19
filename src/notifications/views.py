from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 10

    def get_queryset(self):
        return (
            self.model.objects.filter(user=self.request.user)
            .order_by("-received_at")
            .select_related("notification_user", "notification_group")
        )
