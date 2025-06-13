from django.views.generic import TemplateView


class UserStatsView(TemplateView):
    template_name = "analytics/analytics.html"
