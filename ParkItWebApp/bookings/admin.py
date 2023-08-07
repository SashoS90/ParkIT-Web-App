from django.contrib import admin

from ParkItWebApp.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'parking_spot', 'start_time', 'end_time', 'price', 'created_at', 'duration']
    search_fields = ['id__istartswith', 'user__istartswith',]
