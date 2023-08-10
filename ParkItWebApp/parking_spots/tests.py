from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from ParkItWebApp.parking_spots.forms import RentParkingSpotForm, EditParkingSpotForm
from ParkItWebApp.parking_spots.models import ParkingSpot
from ParkItWebApp.reviews.models import Review

UserModel = get_user_model()


class RentParkingSpotFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'city': 'Sofia',
            'post_code': 1000,
            'district': 'Lagera',
            'street': 'Hadzhi Petko',
            'house_number': 23,
            'type_of_space': 'DRIVEWAY',
            'electric_vehicle_charger': True,
            'hourly_rate': 2.50,
            'status': True,
        }
        form = RentParkingSpotForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = RentParkingSpotForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 8)

    def test_invalid_hourly_rate(self):
        form_data = {
            'city': 'Test City',
            'post_code': '1000',
            'district': 'Test District',
            'street': 'Test Street',
            'house_number': '123',
            'type_of_space': 'DRIVEWAY',
            'electric_vehicle_charger': True,
            'hourly_rate': -10.0,
            'status': True,
        }
        form = RentParkingSpotForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
        self.assertIn('hourly_rate', form.errors)


class EditParkingSpotViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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
            type_of_space='indoor',
            electric_vehicle_charger=True,
            hourly_rate=10.0,
            status=True,
            owner=self.user
        )
        self.edit_parking_spot_url = reverse('edit_parking_spot_page', kwargs={'pk': self.parking_spot.id})

    def test_edit_parking_spot_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.edit_parking_spot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-parking-spot-page.html')
        self.assertIsInstance(response.context['form'], EditParkingSpotForm)
        self.assertEqual(response.context['object'], self.parking_spot)

    def test_edit_parking_spot_view_post_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'city': 'Updated City',
            'post_code': '1000',
            'district': 'Updated District',
            'street': 'Updated Street',
            'house_number': '456',
            'type_of_space': 'DRIVEWAY',
            'electric_vehicle_charger': False,
            'hourly_rate': 15.0,
            'status': False,
        }
        response = self.client.post(self.edit_parking_spot_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        updated_parking_spot = ParkingSpot.objects.get(id=self.parking_spot.id)
        self.assertEqual(updated_parking_spot.city, 'Updated City')
        self.assertEqual(updated_parking_spot.hourly_rate, 15.0)
        self.assertRedirects(response, reverse('parking_spots_list_page', args=[self.user.id]))


class DeleteParkingSpotViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='0886794932'
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
        self.delete_parking_spot_url = reverse('delete_parking_spot_page', kwargs={'pk': self.parking_spot.id})

    def test_delete_parking_spot_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.delete_parking_spot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete-parking-spot-page.html')
        self.assertEqual(response.context['object'], self.parking_spot)

    def test_delete_parking_spot_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.delete_parking_spot_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ParkingSpot.objects.filter(id=self.parking_spot.id).exists())
        self.assertRedirects(response, reverse('parking_spots_list_page', args=[self.user.id]))


class FindParkingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='0886794932'
        )
        self.parking_spot_1 = ParkingSpot.objects.create(
            city='Test City',
            post_code='12345',
            district='Test District',
            street='Test Street 1',
            house_number='123',
            type_of_space='DRIVEWAY',
            electric_vehicle_charger=True,
            hourly_rate=10.0,
            status=True,
            owner=self.user
        )
        self.parking_spot_2 = ParkingSpot.objects.create(
            city='Test City',
            post_code='54321',
            district='Test District',
            street='Test Street 2',
            house_number='456',
            type_of_space='DRIVEWAY',
            electric_vehicle_charger=True,
            hourly_rate=15.0,
            status=True,
            owner=self.user
        )
        self.find_parking_url = reverse('find_parking_page')

    def test_find_parking_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.find_parking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'find-parking-page.html')
        self.assertEqual(len(response.context['all_search_results']), 2)
        self.assertIn(self.parking_spot_1, response.context['all_search_results'])
        self.assertIn(self.parking_spot_2, response.context['all_search_results'])

    def test_find_parking_view_get_with_search_query(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.find_parking_url, {'search': 'Test Street 1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'find-parking-page.html')
        self.assertEqual(len(response.context['all_search_results']), 1)
        self.assertIn(self.parking_spot_1, response.context['all_search_results'])
        self.assertNotIn(self.parking_spot_2, response.context['all_search_results'])


class ParkingSpotDetailsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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
            type_of_space='indoor',
            electric_vehicle_charger=True,
            hourly_rate=10.0,
            status=True,
            owner=self.user
        )
        self.review_1 = Review.objects.create(
            parking_spot=self.parking_spot,
            user=self.user,
            rating=4,
            comment='Test review 1'
        )
        self.review_2 = Review.objects.create(
            parking_spot=self.parking_spot,
            user=self.user,
            rating=5,
            comment='Test review 2'
        )
        self.parking_spot_details_url = reverse('parking_spot_details_page', kwargs={'pk': self.parking_spot.id})

    def test_parking_spot_details_view_get(self):
        response = self.client.get(self.parking_spot_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view-parking-spot-page.html')
        self.assertEqual(response.context['parking_spot'], self.parking_spot)
        self.assertEqual(response.context['reviews_count'], 2)
        self.assertEqual(response.context['rating'], 4.5)
        self.assertIn(self.review_1, response.context['reviews'])
        self.assertIn(self.review_2, response.context['reviews'])

    def test_parking_spot_details_view_get_no_reviews(self):
        self.parking_spot.reviews.all().delete()
        response = self.client.get(self.parking_spot_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view-parking-spot-page.html')
        self.assertEqual(response.context['parking_spot'], self.parking_spot)
        self.assertEqual(response.context['reviews_count'], 0)
        self.assertIsNone(response.context['rating'])
        self.assertEqual(list(response.context['reviews']), [])


class RentParkingSpotViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='0886794911'
        )
        self.rent_parking_spot_url = reverse('rent_parking_spot_page')

    def test_rent_parking_spot_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.rent_parking_spot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent_parking_spot_page.html')
        self.assertIsInstance(response.context['form'], RentParkingSpotForm)

    def test_rent_parking_spot_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'city': 'Test City',
            'post_code': '1000',
            'district': 'Test District',
            'street': 'Test Street',
            'house_number': '123',
            'type_of_space': 'DRIVEWAY',
            'electric_vehicle_charger': True,
            'hourly_rate': 2.42,
            'status': True,
        }
        response = self.client.post(self.rent_parking_spot_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ParkingSpot.objects.filter(
            city='Test City',
            post_code='1000',
            district='Test District',
            street='Test Street',
            house_number='123',
            type_of_space='DRIVEWAY',
            electric_vehicle_charger=True,
            hourly_rate=2.42,
            status=True,
            owner=self.user
        ).exists())
        self.assertRedirects(response, reverse('parking_spots_list_page', args=[self.user.id]))
