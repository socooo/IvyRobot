# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-29 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0005_auto_20181028_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu_log',
            name='menu_sht_desc',
            field=models.CharField(blank=True, max_length=100, verbose_name='菜单图标'),
        ),
        migrations.AlterField(
            model_name='menu_mas',
            name='menu_sht_desc',
            field=models.CharField(blank=True, max_length=100, verbose_name='菜单图标'),
        ),
        migrations.AlterField(
            model_name='menu_mas_tmp',
            name='menu_sht_desc',
            field=models.CharField(blank=True, max_length=100, verbose_name='菜单图标'),
        ),
    ]