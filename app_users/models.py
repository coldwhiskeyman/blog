from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(_('О себе'))
    avatar = models.ImageField(_('Аватар'), upload_to='avatars/', default=None, null=True)

    class Meta:
        verbose_name = _("профиль")
        verbose_name_plural = _("профили")

    def __str__(self):
        return f'{self.user}'
