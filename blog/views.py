import csv
from datetime import datetime

from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    UpdateView
)

from blog.forms import PostForm, PostUploadForm
from blog.models import Image, Post


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    login_url = '/users/login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        self.object.published = self.object.created
        self.object.save()
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(file=image, post=self.object)
        return HttpResponseRedirect(self.get_success_url())


class PostUploadView(LoginRequiredMixin, FormView):
    template_name = 'blog/post_upload_form.html'
    form_class = PostUploadForm
    login_url = '/users/login'

    def form_valid(self, form):
        csvfile = self.request.FILES['file'].read().decode('utf-8').splitlines()
        file_text = csv.DictReader(csvfile)
        posts = []
        for line in file_text:
            text, raw_date = line['TEXT'], line['DATE']
            date = datetime.strptime(raw_date, '%d-%m-%Y')
            posts.append(Post(title=_('Без названия'), text=text, published=date, user=self.request.user))
        Post.objects.bulk_create(posts)

        return super(PostUploadView, self).form_valid(form)

    def get_success_url(self):
        return reverse('post_list')


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    login_url = '/users/login'

    def form_valid(self, form):
        for image in self.request.FILES.getlist('images'):
            Image.objects.create(file=image, post=self.object)
        return super(PostUpdateView, self).form_valid(form)
