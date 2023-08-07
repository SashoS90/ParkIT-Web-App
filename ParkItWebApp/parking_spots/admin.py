from django.contrib import admin

from ParkItWebApp.parking_spots.models import ParkingSpot


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ['id', 'house_number', 'street', 'district', 'city', 'post_code', 'status', 'owner', 'type_of_space']
    list_filter = ['city', 'type_of_space']
    search_fields = ['street__istartswith', 'district__istartswith', 'city__istartswith']
    list_display_links = ['id']
