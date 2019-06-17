# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 02:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180703_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_pass',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='使用者'),
        ),
    ]
