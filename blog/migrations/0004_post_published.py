# Generated by Django 2.2 on 2020-12-19 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20201209_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=None, null=True, verbose_name='Дата публикации'),
        ),
    ]