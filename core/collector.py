# -*- coding:utf-8 -*- 
'''
@author: JM
'''

import six
import pandas as pd
import requests
import time
from threading import Thread
import json

from core.config import basic
from database.postgresql import write_data, read_data

# from urllib.request import urlopen, Request

AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}


class Client(object):
    def __init__(self):
        self.heart_active = True
        self.s = requests.session()
        if six.PY2:
            self.heart_thread = Thread(target=self.send_heartbeat)
            self.heart_thread.setDaemon(True)
        else:
            self.heart_thread = Thread(target=self.send_heartbeat,
                                       daemon=True)

    def keepalive(self):
        if self.heart_thread.is_alive():
            self.heart_active = True
        else:
            self.heart_thread.start()

    def send_heartbeat(self):
        while True:
            if self.heart_active:
                try:
                    response = self.heartbeat()
                    self.check_account_live(response)
                except:
                    self.login()
                time.sleep(100)
            else:
                time.sleep(10)

    def get_data_by_page(self, url):
        self.s.headers.update(AGENT)
        param = dict(
            secondary_intent='',
            condition_id='',
            perpage=100,
        )
        try:
            res = self.s.get(url, params=param)
            res = res.content.decode('utf8')
            res = res[res.find('=') + 1:]
            res = res.replace("pages:", "\"pages\":")
            res = res.replace("data:", "\"data\":")
            res = json.loads(res)
            data = res['data']
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(e)

    def heartbeat(self):
        return self.baseinfo

    def exit(self):
        self.heart_active = False

    def check_login_status(self, return_data):
        if hasattr(return_data, 'get') and return_data.get('error_no') == '-1':
            raise NotLoginError


class NotLoginError(Exception):
    def __init__(self, result=None):
        super(NotLoginError, self).__init__()
        self.result = result

    def heartbeat(self):
        return self.baseinfo


def get_single_org_basic_info(url_format, market):
    page_no = 1
    page_count = 200
    df = pd.DataFrame()
    while True:
        url = url_format
        url = url.replace('${DATE}', '2021-01-22')
        url = url.replace('${MARKET}', market)
        url = url.replace('${PAGE_COUNT}', str(page_count))
        url = url.replace('${PAGE_NO}', str(page_no))
        df_new = client.get_data_by_page(url)
        if df_new is None:
            print("机构列表，获取失败，重试：" + url)
            continue
        if not df_new.empty:
            if not df.empty:
                df = df.append(df_new)
                print(df_new)
            else:
                df = df_new
            page_no += 1
        else:
            print("机构列表，获取数据结束：" + url)
            break
        time.sleep(5)
    return df


def get_all_org_basic_info():
    df_sh = get_single_org_basic_info(url_format=basic['url']['org_basic_info'], market=basic['sh']['market_code'])
    df_sz = get_single_org_basic_info(url_format=basic['url']['org_basic_info'], market=basic['sz']['market_code'])
    if not df_sh.empty and not df_sz.empty:
        df = df_sh.merge(df_sz, on='PARTICIPANTCODE')
    write_data(df, 'org_basic_info')


def get_single_org_stock_info(url_format, org, market_sh, market_sz):
    page_no = 1
    page_count = 200
    org_id = org[0]
    org_name = org[1]
    df = pd.DataFrame()
    while True:
        url = url_format
        url = url.replace('${DATE}', '2021-01-22')
        url = url.replace('${PARTICIPANTCODE}', org_id)
        url = url.replace('${MARKET_SH}', market_sh)
        url = url.replace('${MARKET_SZ}', market_sz)
        url = url.replace('${PAGE_COUNT}', str(page_count))
        url = url.replace('${PAGE_NO}', str(page_no))
        print(org_name+"，机构持仓："+url)
        df_new = client.get_data_by_page(url)
        if df_new is None:
            print(org_name+"机构持仓，获取失败，重试：" + url)
            continue
        if not df_new.empty:
            if not df.empty:
                df = df.append(df_new)
                print(df_new)
            else:
                df = df_new
            page_no += 1
        else:
            print(org_name+"机构持仓，获取数据结束：" + url)
            break
        time.sleep(5)
    return df


def get_all_org_stock_info():
    org_list = read_data("select \"PARTICIPANTCODE\",\"PARTICIPANTNAME_x\" from org_basic_info")
    df = pd.DataFrame()
    for org in org_list.values:
        df_new = get_single_org_stock_info(url_format=basic['url']['org_stock_info'], org=org,
                                       market_sh=basic['sh']['market_code'],
                                       market_sz=basic['sz']['market_code'])
        if not df_new.empty:
            df = df.append(df_new)
    write_data(df, 'org_stock_info')
    return df


if __name__ == '__main__':
    client = Client()
    # get_all_org_basic_info()
    get_all_org_stock_info()
