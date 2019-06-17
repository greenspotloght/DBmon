#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:16:45 2018

@author: webadmin
"""
import string
import random
import datetime
from db import MySQL
from apscheduler.schedulers.blocking import BlockingScheduler as sc
from dbmon.settings_s import *
from linebot import LineBotApi
from linebot.models import TextSendMessage
from pexcept import PrintException


channel_access_token = 'NPLlcG+qwer8xaovWRzvQIZjK3/Q5Y/vREqN75lU2hm1Y0WF04NyfFufzXjzi1PoivQURQ4YCGiEOmPBKq0FNql2/+m3lNgu2rstFifyLTw3M2vQKL5ZfgLkYGLl9X0m4rmYSkfuZ+MruyUQccUrFAdB04t89/1O/w1cDnyilFU='

def id_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def line(group, temp, expire):
    print('send line')

    line_bot_api = LineBotApi(channel_access_token)
    msg = "Temp Passowrd:{} \nExpiretime:\n{}".format(temp, expire)
    try:
        line_bot_api.push_message(group[0], TextSendMessage(text=msg))
    except Exception as e:
        PrintException()
        print('no groupid')




def change():
    with MySQL(pwd=PASSWORD) as DB:
        DB.query('select id from auth_user;')
        ids = DB.fetch('all')
        expire = datetime.datetime.now() + datetime.timedelta(days=1)
        for i in ids:
            temp = id_generator()
            sql = 'insert into Temp_Pass (temp,expiration,user_id) VALUE ("{}","{}","{}") ON DUPLICATE KEY UPDATE temp="{}",expiration="{}"'
            DB.query(sql.format(temp, expire, i[0], temp, expire))
            DB.query('select line_group_id from Company_Admin where id={}'.format(i[0]))
            group = DB.fetch()
            DB.query('select temp from Temp_Pass where user_id={}'.format(i[0]))
            temp = DB.fetch()[0]
            line(group,temp, expire)




if __name__=='__main__':
    print('start crontab')
    sched = sc()
    sched.add_job(change, 'cron', hour= 7,minute = 0)
    sched.start()
