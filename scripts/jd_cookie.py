#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2021/1/2 上午1:46
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : jd_cookie.py
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
from scripts import jd
from setup import get_standard_time
from utils import notify
from utils.configuration import read


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))


def check_valid(cookies):
    try:
        headers = {
            'Host': 'api.m.jd.com',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'User-Agent': 'jdapp;iPhone;8.5.5;13.5;Mozilla/5.0 (iPhone; CPU iPhone OS 13_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1',
            'Accept-Language': 'zh-cn',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        params = {
            'functionId': 'plantBeanIndex',
            'body': json.dumps({
                'monitor_source': 'plant_m_plant_index',
                'version': '8.4.0.0'
            }),
            'appid': 'ld'
        }
        response = requests.get(url='https://api.m.jd.com/client.action', headers=headers, params=params,
                                cookies=cookies).json()
        return response
    except:
        print(traceback.format_exc())
        return


def jd_cookie():
    # 读取 jd_cookie 配置
    config_latest, config_current = read()
    try:
        jd_config = config_current['jobs']['jd']
    except:
        print(traceback.format_exc())
        print('配置文件中没有此任务！请更新您的配置文件')
        return
    # 脚本版本比较
    jd_cookie_config = jd.check_jd_scripts_version(config_latest, config_current, 'jd_cookie')

    if jd_cookie_config['enable']:
        accounts = jd_config['parameters']['ACCOUNTS']
        valid_cookies = []
        for account in accounts:
            utc_datetime, beijing_datetime = get_standard_time()
            symbol = '=' * 16
            print(f'\n{symbol}【京东-ck有效性检测】{utc_datetime.strftime("%Y-%m-%d %H:%M:%S")}/{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} {symbol}\n')
            start_time = time.time()
            title = f'☆【京东-ck有效性检测】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            try:
                # 使用正则找 pt_pin 和 pt_key
                pt_pin = re.findall(r'pt_pin=(.*?);', account['COOKIE'])[0]
                pt_key = re.findall(r'pt_key=(.*?);', account['COOKIE'])[0]
                cookie = {'pt_pin': pt_pin, 'pt_key': pt_key}  # 设置为字典格式
                check_result = check_valid(cookie)  # 访问 api 检测 ck 有效性
                # 有效性判断
                if check_result['code'] == '0':
                    valid_cookies.append(account['COOKIE'])
                    content = f"cookie - {pt_pin} 有效！"
                elif check_result['code'] == '3':
                    content = f"cookie - {pt_pin} 失效！"
                    # ck 失效发送推送
                    if jd_cookie_config['notify']:
                        notify_mode = jd_config['notify_mode']
                        try:
                            notify.send(title=title, content=content, notify_mode=notify_mode)
                        except:
                            print('请确保配置文件的对应的脚本任务中，参数 notify_mode 下面有推送方式\n')
                    else:
                        print('未进行消息推送。如需发送消息推送，请确保配置文件的对应的脚本任务中，参数 notify 的值为 true\n')
                else:
                    content = '请前往 https://github.com/TNanko/Scripts/issues 反馈问题！'
            except:
                content = 'cookie 错误，请重新抓取！'

            content += f'\n🕛耗时：%.2f秒' % (time.time() - start_time)
            content += f'\n如果帮助到您可以点下🌟STAR鼓励我一下，谢谢~'
            print(title)
            print(content)
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数 enable 设置为 true\n')


def main():
    jd_cookie()


if __name__ == '__main__':
    main()
