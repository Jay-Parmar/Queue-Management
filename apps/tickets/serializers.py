from rest_framework import serializers
from apps.tickets.models import Kiosk, Ticket
from apps.tickets import cron


class TicketIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('id',)


class KioskListSerializer(serializers.ModelSerializer):
    last_ticket_assigned = serializers.SerializerMethodField()
    tickets_resolved_today = serializers.SerializerMethodField()

    class Meta:
        model = Kiosk
        fields = '__all__'

    def get_last_ticket_assigned(self, obj):
        return TicketIdSerializer(Ticket.objects.filter(kiosk_id=obj.id).order_by('-created_at').first()).data

    def get_tickets_resolved_today(self, obj):
        return cron.get_number_tickets_solved()

