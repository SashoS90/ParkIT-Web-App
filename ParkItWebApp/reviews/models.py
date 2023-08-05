from enum import Enum

from django.db import models

from ParkItWebApp.accounts.models import UserProfile
from ParkItWebApp.parking_spots.models import ParkingSpot


class RatingPoints(Enum):
    VERY_POOR = 1
    POOR = 2
    GOOD = 3
    VERY_GOOD = 4
    EXCELLENT = 5

    @classmethod
    def choices(cls):
        return [(choice.value, choice.value) for choice in cls]


class Review(models.Model):
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(blank=False, null=False, choices=RatingPoints.choices())
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_reviews")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.parking_spot}"
