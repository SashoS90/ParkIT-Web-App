from django.contrib import admin

from ParkItWebApp.parking_spots.models import ParkingSpot


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ['house_number', 'street', 'city', 'post_code', 'status', 'owner']
