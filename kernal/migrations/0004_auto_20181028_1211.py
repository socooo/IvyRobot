# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-28 12:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0003_auto_20181028_1210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu_mas_tmp',
            old_name='menu_url',
            new_name='menu_long_desc',
        ),
    ]
