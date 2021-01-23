import tushare as ts

# ts.set_token('875e40cd1cc0639a97604eed28fad3851b17570dff2c57daf7a5e4d0')
pro = ts.pro_api('875e40cd1cc0639a97604eed28fad3851b17570dff2c57daf7a5e4d0')

# df = pro.daily(ts_code='000001.SZ', start_date='20200701', end_date='20200718')
# df = pro.daily(ts_code='601933.SH', start_date='20210101', end_date='20210113')

# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
#
# print(data)

# df = pro.daily_basic(ts_code='', trade_date='20180726', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
# print(df)

df = pro.fund_portfolio(ts_code='001753.OF')
print(df)
