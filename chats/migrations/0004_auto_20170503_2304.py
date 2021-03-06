# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 17:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0003_auto_20170503_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiverUser',
        ),
        migrations.RemoveField(
            model_name='message',
            name='senderUser',
        ),
        migrations.AddField(
            model_name='message',
            name='receiver',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
