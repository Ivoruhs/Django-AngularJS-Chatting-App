# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 16:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_auto_20170503_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='receiver',
            new_name='receiverUser',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='sender',
            new_name='senderUser',
        ),
    ]
