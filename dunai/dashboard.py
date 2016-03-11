from django.utils.translation import ugettext_lazy as _
from jet.dashboard.dashboard import Dashboard, DefaultIndexDashboard, AppIndexDashboard
from jet.dashboard.dashboard_modules import google_analytics
from jet.dashboard.modules import DashboardModule
import subprocess


class UptimeModule(DashboardModule):
    title = 'Uptime info'
    template = 'dunai/widgets/uptime.jade'

    def get_context_data(self):
        out, err = subprocess.Popen(['uptime'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        uptimes = map(lambda x: x.strip(','), filter(None, out.strip().split(' '))[-3:])
        return dict(
            uptime=dict(
                load_1=uptimes[0],
                load_5=uptimes[1],
                load_15=uptimes[2]
            )
        )

class CustomIndexDashboard(DefaultIndexDashboard):
    columns = 3

    def init_with_context(self, context):
        super(CustomIndexDashboard, self).init_with_context(context)

        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsTotals)
        self.available_children.append(google_analytics.GoogleAnalyticsVisitorsChart)
        self.available_children.append(google_analytics.GoogleAnalyticsPeriodVisitors)
        self.available_children.append(UptimeModule)
