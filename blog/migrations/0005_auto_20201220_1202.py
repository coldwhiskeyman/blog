# Generated by Django 2.2 on 2020-12-20 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_published'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published'], 'verbose_name': 'пост', 'verbose_name_plural': 'посты'},
        ),
    ]
