'''
Created on 2020年1月30日

@author: JM
'''
import pandas as pd
import tushare as ts
from sqlalchemy import create_engine 

# engine_ts = create_engine('mysql://root:Abcd1234@127.0.0.1:3306/demos?charset=utf8&use_unicode=1')
engine_ts = create_engine('postgresql+psycopg2://postgres:12345678@127.0.0.1/quant')

def read_data(sql):
    # sql = """select \"PARTICIPANTCODE\" from org_basic_info"""
    df = pd.read_sql_query(sql, engine_ts)
    return df

def write_data(df,table):
    df.to_sql(table, engine_ts, index=False, if_exists='replace', chunksize=5000)

def update_data(df):
    pass

def get_data():
    pro = ts.pro_api()
    df = pro.stock_basic()
    return df


if __name__ == '__main__':
#     df = read_data()
    df = get_data()
    write_data(df)
    print(df)