from rest_framework.serializers import ModelSerializer
from apps.tickets.models import Kiosk

class KioskListSerializer(ModelSerializer):
    class Meta:
        model = Kiosk
        fields = '__all__'



