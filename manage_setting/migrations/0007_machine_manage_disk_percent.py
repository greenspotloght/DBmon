# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-09 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_setting', '0006_auto_20180709_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine_manage',
            name='disk_percent',
            field=models.BooleanField(default=1, verbose_name='Use Percentage'),
        ),
    ]
