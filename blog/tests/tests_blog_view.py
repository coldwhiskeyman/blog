from io import BytesIO

from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from django.test import TestCase

from blog.models import Post
from blog.models import Image as PostImage


class BlogListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user('user', password='Qwerty123')

        post1 = Post.objects.create(title='test1', text='testtext1', user=user)
        post1.published = post1.created
        post1.save()

        post2 = Post.objects.create(title='test2', text='testtext2', user=user)
        post2.published = post2.created
        post2.save()

        post_image = BytesIO()
        post_image.name = 'test.png'
        image_file = UploadedFile(file=post_image, name='test.png')
        PostImage.objects.create(file=image_file, post=post1)

    def test_view_blog_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertEqual(len(response.context['post_list']), 2)

    def test_view_blog_detail(self):
        response = self.client.get('/blog/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['object'].id, 1)

    def test_blog_detail_content(self):
        response = self.client.get('/blog/1')
        self.assertContains(response, 'test1')
        self.assertContains(response, 'testtext1')
