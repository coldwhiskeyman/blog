import csv

from django.contrib.auth.models import User
from django.test import TestCase

from blog.models import Post


class UserBlogPublishTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user('user', password='Qwerty123')

        with open('posts.csv', 'w', newline='') as csvfile:
            fieldnames = ['TEXT', 'DATE']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'TEXT': 'test text 1', 'DATE': '01-01-2021'})
            writer.writerow({'TEXT': 'test text 2', 'DATE': '02-01-2021'})
            writer.writerow({'TEXT': 'test text 3', 'DATE': '03-01-2021'})

    def test_csv_post_success(self):
        self.client.login(username='user', password='Qwerty123')
        with open('posts.csv') as csvfile:
            response = self.client.post('/blog/upload', data={'file': csvfile})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/blog/')

        posts = Post.objects.all()
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0].title, 'Без названия')
        self.assertEqual(posts[0].text, 'test text 3')
        post_date = posts[0].published.strftime('%d-%m-%Y')
        self.assertEqual(post_date, '03-01-2021')

    def test_csv_post_fail(self):
        self.client.login(username='user', password='Qwerty123')
        response = self.client.post('/blog/upload')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/post_upload_form.html')

        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)

    def test_csv_post_unregistered(self):
        with open('posts.csv') as csvfile:
            response = self.client.post('/blog/upload', data={'file': csvfile})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/users/login?next=/blog/upload')
        posts = Post.objects.all()
        self.assertEqual(len(posts), 0)
