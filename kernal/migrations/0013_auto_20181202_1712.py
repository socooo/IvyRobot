# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-12-02 17:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0012_auto_20181201_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_log',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_log_user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
