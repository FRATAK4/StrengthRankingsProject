from django.urls import path

from .views import NotificationsTemplateView

urlpatterns = [path("", NotificationsTemplateView.as_view(), name="notifications")]
