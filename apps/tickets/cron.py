import datetime
from django.db.models import Q, Count
from apps.tickets import models

def make_reports(save=True):
    """
    CRON Job to create reports at the end of the day.
    """
    reports = models.Ticket.objects.filter(
        created_at__gte=datetime.date.today()).values('kiosk').annotate(count=Count('id'))
    everyday_report = dict()
    for report in reports:
        everyday_report[report['kiosk'] if report['kiosk'] else 'unresolved'] = report['count']
    
    if save:
        models.Report.objects.create(report=everyday_report)

    return everyday_report


def get_number_tickets_solved() -> int:
    reports = make_reports(save=False)
    total_count = 0
    for kiosk, count in reports.items():
        if isinstance(kiosk, int):
            total_count += count
    return total_count

