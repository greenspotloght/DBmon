# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-06 05:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_setting', '0002_auto_20180705_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='manage_mc',
            name='line',
            field=models.BooleanField(default=0, verbose_name='Line通知'),
        ),
    ]