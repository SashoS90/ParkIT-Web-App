from django.contrib.auth import get_user_model
from django.test import TestCase
from datetime import timedelta, datetime
from ParkItWebApp.bookings.forms import CreateBookingForm
from ParkItWebApp.parking_spots.models import ParkingSpot

UserModel = get_user_model()


class CreateBookingFormTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )
        self.parking_spot = ParkingSpot.objects.create(
            city='Test City',
            post_code='12345',
            district='Test District',
            street='Test Street',
            house_number='123',
            type_of_space='DRIVEWAY',
            electric_vehicle_charger=True,
            hourly_rate=10.0,
            status=True,
            owner=self.user
        )

    def test_valid_form(self):
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        data = {
            'start_time': start_time.strftime('%Y-%m-%dT%H:%M'),
            'end_time': end_time.strftime('%Y-%m-%dT%H:%M'),
        }
        form = CreateBookingForm(data=data)
        self.assertTrue(form.is_valid())
        booking = form.save(commit=False)
        booking.user = self.user
        booking.parking_spot = self.parking_spot
        booking.save()

        self.assertEqual(booking.duration, 2)
        self.assertEqual(booking.price, 20.0)

    def test_invalid_form(self):
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time - timedelta(hours=1)
        data = {
            'start_time': start_time.strftime('%Y-%m-%dT%H:%M'),
            'end_time': end_time.strftime('%Y-%m-%dT%H:%M'),
        }
        form = CreateBookingForm(data=data)
        self.assertFalse(form.is_valid())
