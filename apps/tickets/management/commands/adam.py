import time
import winsound
import win32print
import win32ui
from win32con import *
from PIL import Image, ImageWin
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand
from pyModbusTCP.client import ModbusClient

from apps.tickets.models import Adam, Kiosk, Ticket
from apps.web_sockets import constants as socket_constants
from apps.tickets.cron import get_number_tickets_solved

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


def create_ticket() -> int:
    ticket = Ticket.objects.create()
    print(f":::Ticket no. {ticket.id} is created")
    async_to_sync(layer.group_send)(socket_constants.default_group, {
        'type': 'send.message',
        'message': {'status': 'created', 'info': f":::Ticket no. {ticket.id} is created"}
    })
    assign_ticket_to_kiosk()
    return ticket.id

def assign_ticket_to_kiosk() -> None:
    tickets = Ticket.objects.filter(is_resolved=False).order_by('created_at')
    kiosks = Kiosk.objects.filter(is_available=True).order_by('updated_at')
    updated_tickets = []
    updated_kiosks = []
    for ticket, kiosk in zip(tickets, kiosks):
        print(f":::Ticket no. {ticket.id} is assigned to Kiosk {kiosk.kiosk_number}")
        async_to_sync(layer.group_send)(socket_constants.default_group, {
            'type': 'send.message',
            'message': {'status': 'assigned', 'ticket': f'{ticket.id}', 'kiosk': f'{kiosk.id}', 'total_solved': get_number_tickets_solved()}
        })
        ticket.is_resolved = True
        ticket.kiosk = kiosk
        kiosk.is_available = False
        updated_tickets.append(ticket)
        updated_kiosks.append(kiosk)
    
    
    if len(tickets):
        frequency = 500
        duration = 500
        winsound.Beep(frequency, duration)

    Kiosk.objects.bulk_update(updated_kiosks, ['is_available'])
    Ticket.objects.bulk_update(updated_tickets, ['is_resolved', 'kiosk'])

def make_kiosk_available(adam: Adam):
    kiosk = adam.kiosk
    kiosk.is_available = True
    kiosk.save()

def call_printer(ticket_number: int):
    printer_name = win32print.GetDefaultPrinter()
    try:
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            hDC.StartDoc("Ticket Print Job")
            hDC.StartPage()
            
            x_start, y_start = 25, 0
            ticket_width, ticket_height = 350, 150

            header_font = win32ui.CreateFont({
                'name': 'Arial',
                'height': -24,
                'weight': FW_BOLD,
            })
            
            # Header output
            header = "Prayagraj Nagar Nigam"
            header_width, header_height = hDC.GetTextExtent(header)

            pil_image = Image.open("C:\\Users\\Demo\\Downloads\\pnn_logo.png")
            image_width = header_width // 2
            scale_factor = image_width / pil_image.width
            image_height = int(pil_image.height * scale_factor)
            pil_image_resized = pil_image.resize((image_width, image_height), Image.Resampling.LANCZOS)

            pil_image_gray = pil_image_resized.convert('L')  # Convert to grayscale
            # Convert grayscale to black and white
            threshold = 128 # Threshold can be adjusted
            pil_image_bw = pil_image_gray.point(lambda x: 255 if x > threshold else 0, '1')

            dib = ImageWin.Dib(pil_image_bw)
            image_x_start = x_start + (ticket_width - image_width) // 2  # Center the image

            dib.draw(hDC.GetHandleOutput(), (image_x_start, y_start + 10, image_x_start + image_width, y_start + 10 + image_height))

            # Draw a border
            # hDC.Rectangle((x_start, y_start, x_start + ticket_width, y_start + ticket_height))
            
            header_y_start = y_start + 10 + image_height + 10
            hDC.SelectObject(header_font)
            hDC.TextOut((x_start + (ticket_width - header_width) // 2), header_y_start, header)
            
            ticket_font = win32ui.CreateFont({
                'name': 'Arial',
                'height': -20,
            })
            # Ticket number output
            hDC.SelectObject(ticket_font)
            ticket_info = f"Ticket Number:"
            text_width, text_height = hDC.GetTextExtent(ticket_info)
            hDC.TextOut((x_start + (ticket_width - text_width) // 2), header_y_start + 40, ticket_info)

            ticket_font = win32ui.CreateFont({
                'name': 'Arial',
                'height': -70,
            })
            hDC.SelectObject(ticket_font)
            number_width, number_height = hDC.GetTextExtent(str(ticket_number))
            hDC.TextOut((x_start + (ticket_width - number_width) // 2), header_y_start + 70, str(ticket_number))
            
            hDC.EndPage()
            hDC.EndDoc()
            print(f"Printed Ticket Number: {ticket_number}")
        # except Exception as aaaa:
        #     raise
        finally:
            win32print.ClosePrinter(hPrinter)
    except Exception as e:
        print(f"Failed to print: {e}")

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
                                ticket_id = create_ticket()
                                call_printer(ticket_id)
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
START_ADDRESS = 0
NUM_BUTTONS = 25


class Command(BaseCommand):
    help = 'Listens to specified COM ports and logs data'
    def handle(self, *args, **options):
        monitor_buttons(IP_ADDRESS, PORT, START_ADDRESS, NUM_BUTTONS)


