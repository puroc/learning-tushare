# -*- coding:utf-8 -*- 
'''
Created on 2020年1月30日
@Group: waditu.com
@author: JM
'''

import pandas as pd

def read_data():
    df = pd.read_excel('d:\\20200123.xls', encoding='utf8')
    df.columns = ['code', 'name']
    print(df)


if __name__ == '__main__':
    read_data()