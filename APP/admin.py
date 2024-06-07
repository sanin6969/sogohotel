from django.contrib import admin
from .models import *


# admin.site.register(Hotel)
class RoomAdmin(admin.ModelAdmin):
    list_display=('room_number','room_type','price')
admin.site.register(Payment)
admin.site.register(Ticket)
admin.site.register(Room,RoomAdmin)
