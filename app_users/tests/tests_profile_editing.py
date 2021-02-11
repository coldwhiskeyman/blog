from django.contrib.auth.models import User
from django.test import TestCase

from app_users.models import Profile


class UserProfileEditingTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user('user1',
                                         password='Qwerty123',
                                         first_name='Ivan',
                                         last_name='Ivanov')
        Profile.objects.create(user=user1, bio='I am a test user 1')

        user2 = User.objects.create_user('user2',
                                         password='Qwerty789',
                                         first_name='Petr',
                                         last_name='Petrov')
        Profile.objects.create(user=user2, bio='I am a test user 2')

    def tearDown(self):
        self.client.logout()

    def test_editing_success(self):
        data = {
            'username': 'IvanIvanov',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'bio': 'Я тестовый юзер'
        }
        self.client.login(username='user1', password='Qwerty123')
        user = User.objects.get_by_natural_key(username='user1')
        self.assertEqual(user.username, 'user1')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/{user.id}')
        user = User.objects.get_by_natural_key(username='IvanIvanov')
        self.assertEqual(user.profile.bio, 'Я тестовый юзер')

    def test_anothers_username(self):
        data = {
            'username': 'user2',
        }
        self.client.login(username='user1', password='Qwerty123')
        user = User.objects.get_by_natural_key(username='user1')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'A user with that username already exists')

    def test_invalid_username(self):
        data = {
            'username': '????',
        }
        self.client.login(username='user1', password='Qwerty123')
        user = User.objects.get_by_natural_key(username='user1')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a valid username')

    def test_edit_anothers_profile(self):
        data = {
            'username': 'IvanIvanov',
        }
        self.client.login(username='user1', password='Qwerty123')
        user = User.objects.get_by_natural_key(username='user2')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        User.objects.get_by_natural_key(username='user2')
        self.assertEqual(response.status_code, 403)

    def test_edit_unregistered(self):
        data = {
            'username': 'IvanIvanov',
        }
        user = User.objects.get_by_natural_key(username='user1')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        User.objects.get_by_natural_key(username='user1')
        self.assertEqual(response.status_code, 403)
