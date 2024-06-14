import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from pyModbusTCP.client import ModbusClient

from apps.tickets.models import Adam, Kiosk, Ticket
from apps.web_sockets import constants as socket_constants

layer = get_channel_layer()


class AdamService:
    @staticmethod
    def connect_modbus(host, port):
        modbus_client = ModbusClient(host=host, port=port, auto_open=True)
        return modbus_client

    @staticmethod
    def close_modbus(modbus_client):
        modbus_client.close()

    @staticmethod
    def read_coils(modbus_client, address, count=1):
        return modbus_client.read_coils(address, count)

    @staticmethod
    def write_coils(modbus_client, address, values):
        modbus_client.write_multiple_coils(address, values)


def create_ticket():
    ticket = Ticket.objects.create()
    print(f":::Ticket no. {ticket.id} is created")
    async_to_sync(layer.group_send)(socket_constants.default_group, {
        'type': 'send.message',
        'message': {'status': 'created', 'info': f":::Ticket no. {ticket.id} is created"}
    })
    assign_ticket_to_kiosk()

def assign_ticket_to_kiosk() -> None:
    tickets = Ticket.objects.filter(is_resolved=False).order_by('created_at')
    kiosks = Kiosk.objects.filter(is_available=True).order_by('updated_at')
    updated_tickets = []
    updated_kiosks = []
    for ticket, kiosk in zip(tickets, kiosks):
        print(f":::Ticket no. {ticket.id} is assigned to Kiosk {kiosk.kiosk_number}")
        async_to_sync(layer.group_send)(socket_constants.default_group, {
            'type': 'send.message',
            'message': {'status': 'assigned', 'ticket': f'{ticket.id}', 'kiosk': f'{kiosk.kiosk_number}'}
        })
        ticket.is_resolved = True
        ticket.kiosk = kiosk
        kiosk.is_available = False
        updated_tickets.append(ticket)
        updated_kiosks.append(kiosk)
        # ticket.save()
        # kiosk.save()
    Kiosk.objects.bulk_update(updated_kiosks, ['is_available'])
    Ticket.objects.bulk_update(updated_tickets, ['is_resolved', 'kiosk'])

def make_kiosk_available(adam: Adam):
    kiosk = adam.kiosk
    kiosk.is_available = True
    kiosk.save()

def monitor_buttons(ip, port, start_address, num_buttons):
    modbus_client = AdamService.connect_modbus(ip, port)
    try:
        last_state = [False] * num_buttons  # Initialize last known state
        while True:
            current_state = AdamService.read_coils(modbus_client, start_address, num_buttons)
            if current_state:
                for i, state in enumerate(current_state):
                    if state != last_state[i] and state:
                        print(f"Button {i + start_address} pressed")
                        adam = Adam.objects.filter(ip=ip, port=port, address=i+start_address).first()
                        if adam:
                            if adam.type==Adam.CREATE_TICKET:
                                create_ticket()
                                # call_printer()
                            else:
                                make_kiosk_available(adam)
                                assign_ticket_to_kiosk()
                last_state = current_state
            time.sleep(0.1)  # Polling interval
    finally:
        AdamService.close_modbus(modbus_client)

# Constants for IP, port, etc.
IP_ADDRESS = "192.168.0.81"
PORT = 502
START_ADDRESS = 16
NUM_BUTTONS = 7


class Command(BaseCommand):
    help = 'Listens to specified COM ports and logs data'
    def handle(self, *args, **options):
        monitor_buttons(IP_ADDRESS, PORT, START_ADDRESS, NUM_BUTTONS)


