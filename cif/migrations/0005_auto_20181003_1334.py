# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-03 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cif', '0004_auto_20181003_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cif_tst1',
            name='customer_auto_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cif_id', to='cif.Cif_tst'),
        ),
    ]