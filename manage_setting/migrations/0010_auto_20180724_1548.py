# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-24 07:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_setting', '0009_auto_20180724_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine_manage',
            name='report_time',
            field=models.TimeField(default=datetime.time(0, 0), verbose_name='Make Report Time'),
        ),
    ]
