import os
from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase
from PIL import Image

from app_users.models import Profile


class UserAvatarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('user',
                                        password='Qwerty123',
                                        first_name='Ivan',
                                        last_name='Ivanov')
        Profile.objects.create(user=user, bio='I am a test user')

    def tearDown(self) -> None:
        paths = ['media/avatars/test.png', 'media/avatars/test.txt', 'test.txt']
        for avatar_path in paths:
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

    def test_avatar_upload_success(self):
        self.client.login(username='user', password='Qwerty123')

        avatar = BytesIO()
        image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        image.save(avatar, 'png')
        avatar.name = 'test.png'
        avatar.seek(0)
        data = {
            'username': 'user',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'bio': 'I am a test user',
            'avatar': avatar
        }

        user = User.objects.get_by_natural_key(username='user')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/users/{user.id}')
        user = User.objects.get_by_natural_key(username='user')
        self.assertEqual(user.profile.avatar.name, 'avatars/test.png')

    def test_avatar_fail(self):
        self.client.login(username='user', password='Qwerty123')
        user = User.objects.get_by_natural_key(username='user')

        with open('test.txt', 'w') as file:
            file.write('this is not avatar')

        with open('test.txt') as avatar:
            data = {
                'username': 'user',
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'bio': 'I am a test user',
                'avatar': avatar
            }
            response = self.client.post(f'/users/{user.id}/update', data=data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/user_update.html')
        user = User.objects.get_by_natural_key(username='user')
        self.assertFalse(user.profile.avatar)  # как правильно это проверить?

    def test_avatar_unregistered(self):
        avatar = BytesIO()
        image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        image.save(avatar, 'png')
        avatar.name = 'test.png'
        avatar.seek(0)
        data = {
            'username': 'user',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'bio': 'I am a test user',
            'avatar': avatar
        }

        user = User.objects.get_by_natural_key(username='user')
        response = self.client.post(f'/users/{user.id}/update', data=data)
        self.assertEqual(response.status_code, 403)
        user = User.objects.get_by_natural_key(username='user')
        self.assertFalse(user.profile.avatar)
