# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 18:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='inage',
            new_name='image',
        ),
    ]
