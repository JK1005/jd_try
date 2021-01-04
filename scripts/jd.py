#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2021/1/2 下午1:43
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : jd.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import re
import json
import time
import requests
import traceback
from setup import get_standard_time
from utils import notify
from utils.configuration import read

def check_jd_scripts_version(config_latest, config_current, jd_script_name):
    jd_script_config_current = config_current['jobs']['jd']['scripts'][jd_script_name]
    try:
        jd_config_latest = config_latest['jobs']['jd']
        jd_script_config_latest = jd_config_latest['scripts'][jd_script_name]
        if jd_script_config_current['skip_check_script_version']:
            print('脚本配置参数 skip_check_script_version = true ，跳过脚本版本检测...')
        elif jd_config_latest:
            if jd_config_latest['jobs']['jd']['version'] > config_current['jobs']['jd']['version']:
                print(f"检测到最新的脚本系列版本号为{jd_config_latest['jobs']['jd']['version']}，当前脚本系列版本号：{config_current['jobs']['jd']['version']}")
                if jd_script_config_latest['version'] > jd_script_config_current['version']:
                    print(f"检测到最新的脚本版本号为{jd_script_config_latest['version']}，当前脚本版本号：{jd_script_config_current['version']}")
                else:
                    print('当前脚本为最新版本')
            else:
                print('当前脚本系列为最新版本')
        else:
            print('未获取到最新脚本的版本号')
    except:
        print('程序运行异常，跳过脚本版本检测...')
    finally:
        return jd_script_config_current