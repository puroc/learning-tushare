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

from database.mysql import write_data

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

AGENT = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}

URL = {
    'org_basic': 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=HSGTCOMSTA&token=70f12f2f4f091e459a279469fe49eca5&st=HDDATE,SHAREHOLDCOUNT&sr=3&p=${PAGE_NO}&ps=${PER_PAGE_COUNT}&js=var%20LPMJumVs={pages:(tp),data:(x)}&filter=(MARKET=%27001%27)(HDDATE=^${DATE}^)&rt=53713175'
}


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

    def get_org_basic_info(self, date, page_no=1, page_count=50):
        url = URL['org_basic'].replace('${DATE}', date)
        url = url.replace('${PER_PAGE_COUNT}', str(page_count))
        url = url.replace('${PAGE_NO}', str(page_no))
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
            print(res)
            print(type(res))
            res = json.loads(res)
            print(type(res))
            data = res['data']
            df = pd.DataFrame(data)
            print(df)
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


if __name__ == '__main__':
    client = Client()
    page_no = 1
    page_count = 50
    while True:
        df = client.get_org_basic_info(date='2021-01-22', page_no=page_no, page_count=page_count)
        if not df.empty:
            write_data(df)
            page_no += 1
        else:
            break
        time.sleep(1)
