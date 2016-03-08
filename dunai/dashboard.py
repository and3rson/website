from django.utils.translation import ugettext_lazy as _
from jet.dashboard.dashboard import Dashboard, DefaultIndexDashboard, AppIndexDashboard
from jet.dashboard.dashboard_modules import google_analytics


class CustomIndexDashboard(DefaultIndexDashboard):
    columns = 3

    def init_with_context(self, context):
        super(CustomIndexDashboard, self).init_with_context(context)

        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)
