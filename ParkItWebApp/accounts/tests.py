from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse
from .forms import RegisterUserForm, LoginUserForm, EditProfileForm
from .models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

UserModel = get_user_model()


class UserProfileModelTest(TestCase):

    def test_profile_creation(self):
        user = UserProfile.objects.create(
            username='johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            phone_number='2015551234',
        )
        self.assertEqual(user.username, 'johndoe')
        self.assertEqual(user.first_name, 'John')

    def test_get_full_name(self):
        user = UserProfile(first_name='John', last_name='Doe')
        self.assertEqual(user.get_full_name, 'John Doe')

    def test_profile_picture(self):
        user = UserProfile.objects.create(username='janedoe')
        self.assertEqual(user.profile_picture, None)
        user.profile_picture = 'profile.jpg'
        user.save()
        self.assertEqual(user.profile_picture, 'profile.jpg')

    def test_phone_number_validator(self):
        user = UserProfile(phone_number='abcd')
        self.assertRaises(ValidationError, user.full_clean)

    def test_str_representation(self):
        user = UserProfile(first_name='John', last_name='Doe')
        self.assertEqual(str(user), 'John Doe')


class RegisterFormTest(TestCase):

    def test_valid_data(self):
        form = RegisterUserForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '0886794933'
        })

        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form = RegisterUserForm(data={
            'password1': '1234',
            'password2': '4321',
        })

        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        form = RegisterUserForm(data={
            'email': 'invalid'
        })

        self.assertFalse(form.is_valid())

    def test_required_fields(self):
        form = RegisterUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

    def test_unique_username(self):
        UserProfile.objects.create(username='testuser')

        form = RegisterUserForm(data={
            'username': 'testuser',
        })

        self.assertFalse(form.is_valid())

    def test_unique_email(self):
        UserProfile.objects.create(email='test@example.com')

        form = RegisterUserForm(data={
            'email': 'test@example.com',
        })
        self.assertFalse(form.is_valid())


class EditProfileFormTest(TestCase):

    def test_valid_data(self):
        user = UserProfile.objects.create_user('testuser')
        form = EditProfileForm(instance=user, data={
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'email': 'newemail@test.com',
            'phone_number': '0886794954',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        user = UserProfile.objects.create_user('testuser')
        form = EditProfileForm(instance=user, data={
            'phone_number': '00323667334',
        })
        self.assertFalse(form.is_valid())

    def test_unique_email(self):
        UserProfile.objects.create_user(
            'otheruser',
            email='other@email.com',
            phone_number='0886794953'
        )

        user = UserProfile.objects.create_user(
            'testuser',
            phone_number='0886794950'
        )

        form = EditProfileForm(instance=user, data={
            'email': 'other@email.com',
        })

        self.assertFalse(form.is_valid())

    def test_required_fields(self):
        user = UserProfile.objects.create_user('testuser')
        form = EditProfileForm(instance=user, data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_valid_image_upload(self):
        user = UserProfile.objects.create_user('testuser')
        file = SimpleUploadedFile('test.jpg', b'file_content', 'image/jpeg')
        form = EditProfileForm(instance=user, data={'first_name': 'NewFirstName',
                                                    'last_name': 'NewLastName',
                                                    'email': 'newemail@test.com',
                                                    'phone_number': '0886794954',
                                                    'profile_picture': file})
        self.assertTrue(form.is_valid())


class LoginUserFormTest(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_valid_login(self):
        form_data = {
            "username": "testuser",
            "password": "testpassword",
        }
        form = LoginUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        form_data = {
            "username": "nonexistentuser",
            "password": "testpassword",
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Incorrect username or password. Please check your credentials and try again. "
                      "Alternatively, create a new account.", form.errors["__all__"][0])

    def test_blank_fields(self):
        form_data = {
            "username": "",
            "password": "",
        }
        form = LoginUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required.", form.errors["username"])
        self.assertIn("This field is required.", form.errors["password"])


class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_page')

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register-page.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_register_view_post_valid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '0886794932',
        }
        response = self.client.post(self.register_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertTrue(UserProfile.objects.filter(username='testuser').exists())
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home-page'))

    def test_register_view_post_invalid_data(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'mismatchedpassword',
        }

        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields did not match.")
        self.assertEqual(UserModel.objects.count(), 0)
        self.assertFalse(UserModel.objects.filter(username='testuser').exists())

    def test_register_view_auto_login(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '0886794932'
        }
        response = self.client.post(self.register_url, data, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('home-page'))


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )
        self.edit_profile_url = reverse('edit_profile_page', kwargs={'pk': self.user.id})

    def test_edit_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-profile-page.html')
        self.assertIsInstance(response.context['form'], EditProfileForm)
        self.assertEqual(response.context['user'], self.user)

    def test_edit_profile_view_post_valid_data(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'phone_number': '0886794912',
        }
        response = self.client.post(self.edit_profile_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        updated_user = UserProfile.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertEqual(updated_user.phone_number, '0886794912')
        self.assertRedirects(response, reverse('profile_page', kwargs={'pk': self.user.id}))


class DeleteProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890'
        )
        self.delete_profile_url = reverse('delete_profile_page', kwargs={'pk': self.user.id})

    def test_delete_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.delete_profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete-profile-page.html')
        self.assertEqual(response.context['user'], self.user)

    def test_delete_profile_view_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.delete_profile_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserProfile.objects.filter(username='testuser').exists())
        self.assertRedirects(response, reverse('home-page'))