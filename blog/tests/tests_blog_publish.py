import os
from io import BytesIO

from django.contrib.auth.models import User
from django.test import TestCase
from PIL import Image

from blog.models import Post


class UserBlogPublishTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user', password='Qwerty123')

    def tearDown(self) -> None:
        paths = ['media/images/test1.png', 'media/images/test2.png']
        for image_path in paths:
            if os.path.exists(image_path):
                os.remove(image_path)

    @staticmethod
    def create_test_image(name):
        post_pic = BytesIO()
        image = Image.new('RGB', size=(1, 1), color=(0, 0, 0))
        image.save(post_pic, 'png')
        post_pic.name = f'{name}.png'
        post_pic.seek(0)
        return post_pic

    def test_publish_success(self):
        self.client.login(username='user', password='Qwerty123')

        post_pic1 = self.create_test_image('test1')
        post_pic2 = self.create_test_image('test2')
        data = {
            'title': 'test',
            'text': 'test text',
            'images': (post_pic1, post_pic2),
        }

        response = self.client.post('/blog/add', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/1')

        post = Post.objects.get(id=1)
        self.assertEqual(post.title, 'test')
        self.assertEqual(post.images.all()[0].file.name, 'images/test1.png')

    def test_publish_fail(self):
        self.client.login(username='user', password='Qwerty123')

        data = {
            'title': '',
            'text': '',
        }

        response = self.client.post('/blog/add', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_form.html')
        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)
        self.assertContains(response, 'This field is required')

    def test_publish_unregistered(self):
        data = {
            'title': 'test',
            'text': 'test text',
        }

        response = self.client.post('/blog/add', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login?next=/blog/add')
        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)
