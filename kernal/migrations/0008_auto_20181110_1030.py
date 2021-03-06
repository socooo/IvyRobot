# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-11-10 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kernal', '0007_auto_20181110_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_mas',
            name='employee_id',
            field=models.CharField(default=999999, max_length=50, verbose_name='工号'),
        ),
        migrations.AlterField(
            model_name='user_mas',
            name='address',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='地址'),
        ),
        migrations.AlterIndexTogether(
            name='user_mas',
            index_together=set([('status', 'func', 'maker', 'inp_date', 'checker', 'app_date'), ('employee_id', 'name')]),
        ),
    ]
