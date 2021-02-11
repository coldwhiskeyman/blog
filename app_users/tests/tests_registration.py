from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase
from PIL import Image


class UserRegistrationTests(TestCase):
    def test_minimum_registration_success(self):
        data = {
            'username': 'user',
            'password1': 'Very1Secret2Password3',
            'password2': 'Very1Secret2Password3',
        }
        response = self.client.post('/users/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, 'user')

    def test_full_registration_success(self):
        avatar = BytesIO()
        image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        image.save(avatar, 'png')
        avatar.name = 'test.png'
        avatar.seek(0)

        data = {
            'username': 'user',
            'password1': 'Very1Secret2Password3',
            'password2': 'Very1Secret2Password3',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'bio': 'I am a test user',
            'avatar': avatar,
        }
        response = self.client.post('/users/register', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].profile.bio, 'I am a test user')

    def test_registration_fail(self):
        data = {
            'username': 'user',
            'password1': 'Very1Secret2Password3',
            'password2': 'Very4Secret5Password6',
        }
        response = self.client.post('/users/register', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/register.html')
        users = User.objects.all()
        self.assertEqual(len(users), 0)
        self.assertContains(response, 'The two password fields didn&#39;t match')
