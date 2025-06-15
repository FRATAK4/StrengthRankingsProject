from django.urls import path

from .views import UserStatsView

urlpatterns = [path("<int:pk>/", UserStatsView.as_view(), name="analytics")]
