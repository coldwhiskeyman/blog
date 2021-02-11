from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label=_('Имя'), max_length=30, required=False)
    last_name = forms.CharField(label=_('Фамилия'), max_length=30, required=False)
    avatar = forms.ImageField(label=_('Аватар'), required=False)
    bio = forms.CharField(label=_('О себе'), widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar', 'first_name', 'last_name', 'bio']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label=_('Имя'), max_length=30, required=False)
    last_name = forms.CharField(label=_('Фамилия'), max_length=30, required=False)
    avatar = forms.ImageField(label=_('Аватар'), required=False)
    bio = forms.CharField(label=_('О себе'), widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'avatar', 'first_name', 'last_name', 'bio']
