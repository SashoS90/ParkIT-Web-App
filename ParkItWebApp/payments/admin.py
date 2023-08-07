from django.contrib import admin

from ParkItWebApp.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'amount', 'date_completed', 'user']
