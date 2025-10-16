from django.contrib import admin

from app.models import Event, Reservation
class EventAdmin(admin.ModelAdmin):
    exclude = ('free_seats',)
    def save_model(self, request, obj, form, change):
        obj.free_seats = obj.capacity
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Event,EventAdmin)
admin.site.register(Reservation)