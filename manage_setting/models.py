from django.db import models
from accounts.models import company_admin
from django.contrib.auth.models import User

import datetime

# Create your models here.

class machine_manage(models.Model):
    hostname = models.CharField(verbose_name='hostname', max_length=150, blank=True)
    ip = models.GenericIPAddressField(verbose_name='IP')
    company = models.ForeignKey(company_admin, verbose_name='公司')
    cpu_limit = models.IntegerField(verbose_name='cpu_limit', default=80, max_length=3)
    disk_percent = models.BooleanField(verbose_name='Disk Use Percentage', default=1)
    disk_limit = models.FloatField(verbose_name='disk_limit(GB)', default=10, max_length=4)
    report_time = models.TimeField(verbose_name='Make Report Time', default=datetime.time(0,0,0))
    line = models.BooleanField(verbose_name='Line通知', default=0)

    class Meta:
        db_table = 'manage_mc'
    def __str__(self):
        return self.hostname
