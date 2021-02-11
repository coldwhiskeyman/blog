from django import forms
from django.utils.translation import gettext_lazy as _

from blog.models import Post


class PostUploadForm(forms.Form):
    file = forms.FileField(label=_('CSV-файл'))


class PostForm(forms.ModelForm):
    images = forms.ImageField(label=_('Картинки'), widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ['title', 'text', 'images']
