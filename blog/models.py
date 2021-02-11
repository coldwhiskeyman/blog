from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(_('Заголовок'), max_length=100)
    text = models.TextField(_('Текст'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('Автор'))
    created = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    published = models.DateTimeField(_('Дата публикации'), null=True, default=None)

    def __str__(self):
        return f'{self.user}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_details', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-published']
        verbose_name = _("пост")
        verbose_name_plural = _("посты")


class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images', verbose_name=_('Пост'), default=None)

    def __str__(self):
        return self.file.name

    class Meta:
        verbose_name = _("Картинка")
        verbose_name_plural = _("Картинки")
