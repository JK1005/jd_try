#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/31 上午2:05
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : 52pojie.py
# @Software: PyCharm
import sys
import os

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import time
import requests
import traceback
from bs4 import BeautifulSoup
from setup import get_standard_time, BASE_DIR
from utils import notify, log
from utils.configuration import read


def signin(headers):
    url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2&mobile=no'
    # url = 'https://www.52pojie.cn/home.php?mod=task&do=apply&id=2'
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_nickname(headers):
    try:
        url = 'https://www.52pojie.cn'
        responese = requests.get(url=url, headers=headers)
        bs_obj = BeautifulSoup(responese.text, 'html.parser')
        a = bs_obj.find_all('a', attrs={'target': '_blank', 'title': '访问我的空间'})[0].get_text()
        if a:
            return a
        else:
            return
    except:
        return


def five2pojie():
    # 读取 52破解 配置
    config_latest, config_current = read()
    try:
        five2_config = config_current['jobs']['52pojie']
    except:
        print('配置文件中没有此任务！请更新您的配置文件')
        return
    # 脚本版本检测
    try:
        if five2_config['skip_check_script_version']:
            print('脚本配置参数 skip_check_script_version = true ，跳过脚本版本检测...')
        elif config_latest:
            if config_latest['jobs']['52pojie']['version'] > five2_config['version']:
                print(
                    f"检测到最新的脚本版本号为{config_latest['jobs']['52pojie']['version']}，当前脚本版本号：{five2_config['version']}")
            else:
                print('当前脚本为最新版本')
        else:
            print('未获取到最新脚本的版本号')
    except:
        print('程序运行异常，跳过脚本版本检测...')

    if five2_config['enable']:
        # 获取config.yml账号信息
        accounts = five2_config['parameters']['ACCOUNTS']
        # 脚本名字
        scripts_filename = five2_config['scripts_filename']
        # 日志相关参数
        log_parameters = five2_config['log']

        for account in accounts:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Referer": "https://www.52pojie.cn/index.php",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,pl;q=0.4",
                'Cookie': account['COOKIE'],
            }
            utc_datetime, beijing_datetime = get_standard_time()
            start_time = time.time()

            title = f'☆【吾爱破解】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            account_title = f"\n{'=' * 16}【吾爱破解】{utc_datetime.strftime('%Y-%m-%d %H:%M:%S')}/{beijing_datetime.strftime('%Y-%m-%d %H:%M:%S')} {'=' * 16}\n{title}"
            signin(headers=headers)
            nickname = get_nickname(headers=headers)
            time.sleep(10)
            signin_result = signin(headers=headers)
            if signin_result:
                bs_obj = BeautifulSoup(signin_result, 'html.parser')
                # 获取签到结果所在的 div 标签
                div = bs_obj.find_all('div', attrs={'class': 'alert_info', 'id': "messagetext"})
                # 获取签到结果内容
                result = div[0].find_all('p')[0].get_text()
                if result == '抱歉，本期您已申请过此任务，请下期再来' and nickname:
                    content = '【吾爱破解】%s 签到成功！' % nickname
                elif result == '您需要先登录才能继续本操作':
                    content = '【吾爱破解】cookie 过期！'
                else:
                    content = '【吾爱破解】签到失败！请带着日志前往 https://github.com/TNanko/Scripts/issues 反馈问题！'
            else:
                content = '【吾爱破解】网络错误！'
            content += f'\n🕛耗时：%.2f秒\n如果帮助到您可以点下🌟STAR鼓励我一下，谢谢~' % (time.time() - start_time)

            if log_parameters['enable']:
                try:
                    # folder_path = os.path.join(BASE_DIR, 'log')  # 可能 windows 系统不适用（未测试）
                    folder_path = BASE_DIR + f'/log/{scripts_filename[:-3]}'
                    if not os.path.isdir(folder_path):
                        print('对应的日志文件夹不存在，创建日志文件夹...')
                        os.makedirs(folder_path)
                    beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    log_path = folder_path + '/%s.log' % beijing_datetime.strftime('%Y-%m-%d')
                    # 写入日志
                    log.write_scripts_log(path=log_path, msg='%s\n\n%s' % (account_title, content))
                    # 删除过期日志
                    log.delete_scripts_log(path=folder_path, valid_period=log_parameters['valid_period'])
                except:
                    print('写入日志失败！%s\n%s' % (account_title, content))
            else:
                print(account_title + content)

            if five2_config['notify']:
                # 消息推送方式
                notify_mode = five2_config['notify_mode']
                try:
                    # 推送消息
                    notify.send(title=title, content=content, notify_mode=notify_mode)
                except:
                    print('请确保配置文件的对应的脚本任务中，参数 notify_mode 下面有推送方式\n')
            else:
                print('未进行消息推送。如需发送消息推送，请确保配置文件的对应的脚本任务中，参数 notify 的值为 true\n')
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数 enable 设置为 true\n')


def main():
    five2pojie()


if __name__ == '__main__':
    main()

# 105c币
