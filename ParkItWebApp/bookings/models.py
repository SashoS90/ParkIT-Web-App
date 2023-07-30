from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from ParkItWebApp.accounts.models import UserProfile
from ParkItWebApp.parking_spots.models import ParkingSpot
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from ParkItWebApp.payments.models import Payment


class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="bookings")
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=False, null=False)
    end_time = models.DateTimeField(blank=False, null=False)
    duration = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time must be greater than start time.")
            else:
                duration = self.end_time - self.start_time
                self.duration = duration.total_seconds() // 3600

    def save(self, *args, **kwargs):
        if self.pk is None:
            parking_spot = self.parking_spot
            hourly_rate = parking_spot.hourly_rate
            self.price = hourly_rate * self.duration

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking ID: {self.id}"


@receiver(post_delete, sender=Booking)
def update_parking_spot_status(sender, instance, **kwargs):
    parking_spot = instance.parking_spot
    parking_spot.status = True
    parking_spot.save()


@receiver(post_save, sender="bookings.Booking")
def create_payment(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        Payment.objects.create(booking=instance, amount=instance.price, user=user)

