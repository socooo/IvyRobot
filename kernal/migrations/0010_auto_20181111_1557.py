# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-11-11 15:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0009_auto_20181110_1037'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_mas_tmp',
            options={'ordering': ('employee_id',)},
        ),
        migrations.RemoveField(
            model_name='user_mas_tmp',
            name='user',
        ),
    ]
