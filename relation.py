import pandas as pd
from pandas import Series, DataFrame
import datetime
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl

def mavg_plot(close_px,day):
    mavg = close_px.rolling(window=day).mean()
    mpl.rc('figure', figsize=(8, 7))
    mpl.__version__
    # Adjusting the style of matplotlib
    style.use('ggplot')
    close_px.plot(label=stock_num)
    mavg.plot(label='mavg')
    plt.legend()
    plt.show()    

def rets_plot(close_px,shift):
    rets = close_px / close_px.shift(shift) - 1
    rets.plot(label='return')
    plt.show()


today= datetime.datetime(2020, 8, 18)
date_string='{:%m-%d-%Y}'.format(today)

path="C:\\Users\\kinsonp\\Documents\\GitHub\\stock\\data\\historical_data\\08-18-2020\\"
stocks=[]
for i in range(1,6):
    try:
        stock_num="{:04d}".format(i)
        df =  pd.read_csv(path+stock_num+".csv")
        close_px = df['Adj Close']
        close_px.rename(columns={'Adj Close':stock_num}, inplace=True)
 
        stocks.append(close_px)
        #mavg_plot(close_px,30)
        #rets_plot(close_px,1)
        
    except:
        pass
dfcomp=pd.concat(stocks, axis=1)

retscomp = dfcomp.pct_change()
print(list(retscomp.columns.values))
corr = retscomp.corr()
#print(corr)
plt.scatter(retscomp[0], retscomp[1])
plt.xlabel("Returns 0001")
plt.ylabel("Returns 0002")
plt.show()