from django.urls import path
from apps.tickets.views import KioskListAPI

urlpatterns = [
    path("", KioskListAPI.as_view()),
]
