import datetime
from django.db.models import Q, Count
from apps.tickets import models

def make_reports():
    """
    CRON Job to create reports at the end of the day.
    """
    reports = models.Ticket.objects.filter(
        created_at__gte=datetime.date.today()-datetime.timedelta(days=1)).values('kiosk').annotate(count=Count('id'))
    everyday_report = dict()
    for report in reports:
        everyday_report[report['kiosk'] if report['kiosk'] else 'unresolved'] = report['count']
    models.Report.objects.create(report=everyday_report)


