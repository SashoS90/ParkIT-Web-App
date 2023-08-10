from django import forms
from ParkItWebApp.bookings.models import Booking


class CreateBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user', 'parking_spot', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '1800'})
        self.fields['end_time'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': '1800'})
        self.fields['duration'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
