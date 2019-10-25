# Generated by Django 2.2 on 2019-07-06 13:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0002_auto_20190611_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='likers',
            field=models.ManyToManyField(related_name='likers', to=settings.AUTH_USER_MODEL),
        ),
    ]