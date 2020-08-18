import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
import os
import sys
from datetime import date
from datetime import timedelta

today = date.today()
start = today - timedelta(days=365)
end = today
date_string='{:%m-%d-%Y}'.format(today)
script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
path=script_dir+'\\'+'data'+'\\'+"historical_data\\"+date_string
print(path)
try:
    os.mkdir(path)
except:
    pass
for i in range(6,8):
    try:
        stock_num="{:04d}".format(i)
        print(stock_num)
        df = web.DataReader(stock_num+".HK", 'yahoo', start, end)

        df.to_csv(path+'/'+stock_num+".csv", index=True)
        print(stock_num+" success")
    except:
        pass
print("finish")