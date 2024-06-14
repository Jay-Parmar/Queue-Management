from django.db import models


class Kiosk(models.Model):
    kiosk_number = models.IntegerField(unique=True)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(help_text="Additional Information about the Kiosk")

    def __str__(self) -> str:
        return f"{self.id} - {self.body}"


class Adam(models.Model):
    CREATE_TICKET = 'CREATE_TICKET'
    ASSIGN_KIOSK = 'ASSIGN_KIOSK'
    TYPE_CHOICES = [
        (CREATE_TICKET, 'CREATE_TICKET'),
        (ASSIGN_KIOSK, 'ASSIGN_KIOSK'),
    ]
    ip = models.GenericIPAddressField(null=False, blank=False)
    port = models.IntegerField(default=502)
    address = models.IntegerField(default=16,null=False,blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True, choices=TYPE_CHOICES)
    kiosk = models.ForeignKey(Kiosk, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.id} - {self.ip} - {self.port} - {self.address} - {self.name}"


class Ticket(models.Model):
    kiosk = models.ForeignKey(Kiosk, null=True, blank=True, on_delete=models.SET_NULL)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



