from django.db import models
from enum import Enum
from django.core.validators import MinLengthValidator, MinValueValidator
from .validators import post_code_validator
from django.db.models.signals import post_save
from django.dispatch import receiver
from ParkItWebApp.accounts.models import UserProfile
from django.utils import timezone


@receiver(post_save, sender='bookings.Booking')
def update_parking_spot_status(sender, instance, created, **kwargs):
    if created:
        instance.parking_spot.status = False
        instance.parking_spot.save()
    else:
        if instance.end_time < timezone.now():
            instance.parking_spot.status = True
            instance.parking_spot.save()


class SpaceTypes(Enum):
    DRIVEWAY = 'Driveway'
    CAR_PARK = 'Car Park'
    GARAGE = 'Garage'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


STATUS_CHOICES = [
    (True, 'Available'),
    (False, 'Unavailable'),
]


class ParkingSpot(models.Model):
    city = models.CharField(max_length=20,
                            blank=False,
                            null=False,
                            validators=[MinLengthValidator(2)])
    post_code = models.CharField(blank=False, null=False, validators=[post_code_validator])
    district = models.CharField(blank=False, null=False, max_length=40)
    street = models.CharField(max_length=50,
                              blank=False,
                              null=False,
                              validators=[MinLengthValidator(2)])
    house_number = models.CharField(max_length=10,
                                    blank=False,
                                    null=False)
    type_of_space = models.CharField(choices=SpaceTypes.choices(),
                                     blank=False,
                                     null=False)
    electric_vehicle_charger = models.BooleanField(blank=False,
                                                   null=False)
    hourly_rate = models.FloatField(blank=False,
                                    null=False,
                                    validators=[MinValueValidator(0.01)])
    status = models.BooleanField(blank=False,
                                 null=False,
                                 choices=STATUS_CHOICES)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="parking_spots")
    image = models.ImageField(blank=True, null=True)

    @property
    def get_full_address(self):
        return f"{self.house_number}, {self.street}, {self.district}, {self.city}"

    def __str__(self):
        return f"{self.house_number} {self.street} {self.city} {self.post_code}"