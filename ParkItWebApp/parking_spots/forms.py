from django import forms

from ParkItWebApp.parking_spots.models import ParkingSpot


class BaseParkingSpotModelForm(forms.ModelForm):
    class Meta:
        model = ParkingSpot
        exclude = ['owner']


class RentParkingSpotForm(BaseParkingSpotModelForm):
    pass


class EditParkingSpotForm(BaseParkingSpotModelForm):
    pass
