import os
from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase
from PIL import Image

from blog.models import Post


class UserBlogPublishTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('user', password='Qwerty123')
        post = Post.objects.create(title='test', text='test text', user=user)
        post.published = post.created
        post.save()

    def tearDown(self) -> None:
        image_path = 'media/images/test.png'
        if os.path.exists(image_path):
            os.remove(image_path)

    def test_update_success(self):
        self.client.login(username='user', password='Qwerty123')

        post_pic = BytesIO()
        image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        image.save(post_pic, 'png')
        post_pic.name = 'test.png'
        post_pic.seek(0)
        data = {
            'title': 'new title',
            'text': 'new text',
            'images': post_pic,
        }

        response = self.client.post('/blog/1/update', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/1')
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'new title')
        self.assertEqual(post.images.all()[0].file.name, 'images/test.png')

    def test_update_fail(self):
        self.client.login(username='user', password='Qwerty123')

        data = {
            'title': '',
            'text': '',
        }

        response = self.client.post('/blog/1/update', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
        self.assertContains(response, 'This field is required')
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'test')

    def test_publish_unregistered(self):
        data = {
            'title': 'new title',
            'text': 'new text',
        }

        response = self.client.post('/blog/1/update', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login?next=/blog/1/update')
        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'test')
