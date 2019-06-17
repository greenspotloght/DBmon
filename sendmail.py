# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:24:39 2017

@author: Artin
"""

from django.core.mail import send_mail

#################寄信程式,利用django內建模組#####################
def sendmail(subject, message, emailto):
    send_mail(
        subject,
        message,
        'line@greensyslog.com',
        emailto,
        fail_silently=False,
    )
###############################################################
