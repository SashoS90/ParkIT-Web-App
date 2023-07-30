from django.contrib import admin

from ParkItWebApp.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['parking_spot', 'rating', 'comment']
