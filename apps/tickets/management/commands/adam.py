from django.core.management.base import BaseCommand
from pyModbusTCP.client import ModbusClient
import time

from apps.tickets.models import Adam, Kiosk, Ticket

# delay = 0.2
# adam_objects = Adam.objects.all()

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

def assign_ticket_to_kiosk() -> None:
    tickets = Ticket.objects.filter(is_resolved=False).order_by('created_at')
    kiosks = Kiosk.objects.filter(is_available=True).order_by('updated_at')
    for ticket, kiosk in zip(tickets, kiosks):
        print(f":::Ticket no. {ticket.id} is assigned to Kiosk {kiosk.kiosk_number}")
        ticket.is_resolved = True
        ticket.kiosk = kiosk
        kiosk.is_available = False
        ticket.save()
        kiosk.save()

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
                    if state != last_state[i]:
                        if state:
                            print(f"Button {i + start_address} pressed")
                            adams = Adam.objects.filter(ip=ip, port=port, address=i+start_address)
                            if adams:
                                adam_type = adams.first().type
                                if adam_type==Adam.CREATE_TICKET:
                                    create_ticket()
                                    # call_printer()
                                else:
                                    make_kiosk_available(adams.first())
                                    assign_ticket_to_kiosk()
                        # else:
                        #     print(f"Button {i + start_address} released")
                        # Example action on press
                        # AdamService.write_coils(modbus_client, start_address + i, [not state])
                last_state = current_state
            time.sleep(0.1)  # Polling interval
    finally:
        AdamService.close_modbus(modbus_client)

# Constants for IP, port, etc.
IP_ADDRESS = "192.168.0.81"
PORT = 502
START_ADDRESS = 16  # Update with the correct starting address for your buttons
NUM_BUTTONS = 7  # Total number of buttons


class Command(BaseCommand):
    help = 'Listens to specified COM ports and logs data'
    def handle(self, *args, **options):
        monitor_buttons(IP_ADDRESS, PORT, START_ADDRESS, NUM_BUTTONS)


