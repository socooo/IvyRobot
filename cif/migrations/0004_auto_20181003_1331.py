# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-10-03 13:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cif', '0003_auto_20181003_1330'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='cif_tst2',
            index_together=set([]),
        ),
        migrations.RemoveField(
            model_name='cif_tst2',
            name='customer_auto_id2',
        ),
        migrations.DeleteModel(
            name='Cif_tst2',
        ),
    ]
