from django.shortcuts import render
from django.views.generic import TemplateView


class NotificationsTemplateView(TemplateView):
    template_name = "notifications/notification-list.html"
