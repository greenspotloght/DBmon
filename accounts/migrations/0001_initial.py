# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-15 05:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='company_admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30, verbose_name='公司名稱')),
                ('company_id', models.IntegerField(unique=True, verbose_name='公司統編')),
                ('company_tel', models.CharField(blank=True, max_length=20, null=True, verbose_name='公司電話')),
                ('company_fax', models.IntegerField(blank=True, null=True, verbose_name='公司傳真')),
                ('company_ip', models.GenericIPAddressField(unique=True, verbose_name='公司IP位址')),
                ('company_ip2', models.GenericIPAddressField(null=True, unique=True, verbose_name='公司IP位址2')),
                ('company_ip3', models.GenericIPAddressField(null=True, unique=True, verbose_name='公司IP位址3')),
                ('company_address', models.TextField(verbose_name='公司地址')),
                ('company_db', models.CharField(blank=True, max_length=12, null=True, verbose_name='公司資料庫')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='加入日期')),
                ('date_expiration', models.DateField(verbose_name='有效日期')),
                ('is_active', models.BooleanField(verbose_name='使用中')),
                ('line_group_id', models.CharField(blank=True, max_length=33, null=True, verbose_name='Line群組ID')),
                ('principal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='公司帳戶管理帳戶')),
            ],
            options={
                'verbose_name': '公司資訊',
                'verbose_name_plural': '公司資訊',
                'db_table': 'Company_Admin',
            },
        ),
        migrations.CreateModel(
            name='company_user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, verbose_name='使用者帳戶')),
                ('line_user_id', models.CharField(blank=True, max_length=33, null=True, verbose_name='Line使用者ID')),
                ('company_admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company_admin', verbose_name='所屬公司')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            options={
                'verbose_name': '公司與使用者',
                'verbose_name_plural': '公司與使用者',
                'db_table': 'Company_User',
            },
        ),
        migrations.CreateModel(
            name='suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='主旨')),
                ('suggestion', models.TextField(verbose_name='建議')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            options={
                'verbose_name': '意見回饋',
                'verbose_name_plural': '意見回饋',
                'db_table': 'suggestion',
            },
        ),
        migrations.CreateModel(
            name='User_Verify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('captcha', models.CharField(max_length=6, verbose_name='認證碼')),
                ('is_verify', models.BooleanField(default=0, verbose_name='已認證')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='使用者')),
            ],
            options={
                'verbose_name': '使用者認證',
                'verbose_name_plural': '使用者認證',
                'db_table': 'User_Verify',
            },
        ),
    ]
