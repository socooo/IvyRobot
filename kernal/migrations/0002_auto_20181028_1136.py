# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-28 11:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='role_log',
            name='menu',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Role_log_menu_id', to='kernal.Menu_mas'),
        ),
        migrations.AddField(
            model_name='role_mas',
            name='menu',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Role_mas_menu_id', to='kernal.Menu_mas'),
        ),
    ]
