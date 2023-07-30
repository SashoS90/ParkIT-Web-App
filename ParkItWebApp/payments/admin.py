from django.contrib import admin

from ParkItWebApp.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['booking', 'amount', 'date_completed']
