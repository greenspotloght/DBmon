# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180703_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_pass',
            name='expiration',
            field=models.DateTimeField(blank=True, verbose_name='有效日期'),
        ),
    ]