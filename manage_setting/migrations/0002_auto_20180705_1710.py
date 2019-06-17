# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 09:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_setting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='manage_mc',
            name='cpu_limit',
            field=models.IntegerField(default=80, max_length=3, verbose_name='cpu_limit'),
        ),
        migrations.AddField(
            model_name='manage_mc',
            name='disk_limit',
            field=models.IntegerField(default=10, max_length=3, verbose_name='disk_limit'),
        ),
    ]
