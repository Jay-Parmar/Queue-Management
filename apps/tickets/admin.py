# Register your models here.
from django.contrib import admin
from .models import Adam, Kiosk, Ticket, Report


class KioskAdmin(admin.ModelAdmin):
    readonly_fields = ('updated_at',)


class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

# admin.site.register(Rating,RatingAdmin)

admin.site.register(Adam)
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Report, ReportAdmin)


