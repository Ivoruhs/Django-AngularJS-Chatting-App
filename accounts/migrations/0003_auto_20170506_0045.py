# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 18:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20170506_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='userId',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
