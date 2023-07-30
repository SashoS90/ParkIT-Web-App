from django.conf import settings
from django.db import models


class Payment(models.Model):
    booking = models.OneToOneField("bookings.Booking", on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_completed = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.amount is None:
            self.amount = self.booking.price

        super().save(*args, **kwargs)

    @property
    def get_booking(self):
        return f"{self.booking}"

    def __str__(self):
        return f"Transaction ID: {self.id}"
