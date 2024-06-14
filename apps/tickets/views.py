from rest_framework.generics import ListAPIView
from apps.tickets.serializers import KioskListSerializer
from apps.tickets.models import Kiosk

# Create your views here.

class KioskListAPI(ListAPIView):
    serializer_class = KioskListSerializer
    queryset = Kiosk.objects.all()

