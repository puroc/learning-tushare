# -*- coding:utf-8 -*- 
'''
Created on 2020年1月30日
@Group: waditu.com
@author: JM
'''
import time
import pandas as pd
import tushare as ts

class MarketData(object):
    def __init__(self):
        self.pro = ts.pro_api()
                 
                 
    def daily(self, ts_code='', trade_date='', start_date='', end_date=''):
        if trade_date:
            df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
        else:
            df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df


    def daily_strong(self, ts_code='', trade_date='', start_date='', end_date=''):
        for _ in range(5):
            try:
                if trade_date:
                    df = self.pro.daily(ts_code=ts_code, trade_date=trade_date)
                else:
                    df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            except:
                print('pause')
                time.sleep(1)
            else:
                return df


if __name__ == '__main__':
    market = MarketData()
    date_range = pd.date_range(start='20200101', end='20200123', freq='B')
    for date in date_range:
        date = str(date)[0:10].replace('-', '')
        print(date)
        df = market.daily_strong(trade_date=date)
        print(df)