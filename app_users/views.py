from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView

from app_users.forms import RegisterForm, UserUpdateForm
from app_users.models import Profile


class UserLoginView(LoginView):
    template_name = 'app_users/login.html'

    def get_success_url(self):
        return reverse('index')


class UserLogoutView(LogoutView):
    next_page = '/'


class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'app_users/register.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        bio = form.cleaned_data.get('bio')
        user = form.save()
        avatar = None
        if self.request.FILES:
            avatar = self.request.FILES['avatar']
        Profile.objects.create(user=user, bio=bio, avatar=avatar)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'app_users/user_detail.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'app_users/user_update.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id == kwargs['pk']:
            return super(UserUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        bio = form.cleaned_data.get('bio')
        user = self.request.user

        profile, created = Profile.objects.get_or_create(defaults={'bio': bio}, user=user)
        profile.bio = bio

        if self.request.FILES:
            profile.avatar = self.request.FILES['avatar']

        profile.save()

        return super().form_valid(form)
    
    def get_initial(self):
        self.initial = super(UserUpdateView, self).get_initial()
        try:
            self.initial['bio'] = self.request.user.profile.bio
        except User.profile.RelatedObjectDoesNotExist:
            pass
        return self.initial
