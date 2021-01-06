#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/11/29 17:08
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : setup.py
# @Software: PyCharm

import os
BASE_DIR = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0]
from datetime import datetime, timezone, timedelta
from bin import schedule


def get_standard_time():
    """
    获取utc时间和北京时间
    :return:
    """
    # <class 'datetime.datetime'>
    utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
    beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
    return utc_datetime, beijing_datetime


def setup_crontab():
    print('【删除项目旧定时任务...】')
    schedule.delete_cron()
    print('【创建项目定时任务...】')
    schedule.create_cron(skip_check_version=True)


if __name__ == '__main__':
    leam = '''
         ,dPYb,                                        
         IP'`Yb                                        
         I8  8I                                        
         I8  8'                                        
         I8 dP   ,ggg,     ,gggg,gg   ,ggg,,ggg,,ggg,  
         I8dP   i8" "8i   dP"  "Y8I  ,8" "8P" "8P" "8, 
         I8P    I8, ,8I  i8'    ,8I  I8   8I   8I   8I 
        ,d8b,_  `YbadP' ,d8,   ,d8b,,dP   8I   8I   Yb,
        8P'"Y88888P"Y888P"Y8888P"`Y88P'   8I   8I   `Y8
    '''
    print(leam)
    print('【开始安装 TNanko Scripts ...】')
    setup_crontab()
    print('【安装成功！】')
