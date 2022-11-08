import pandas as pd
from pandas import DataFrame
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import os

directory='C:/Users/zanna/.spyder-py3/New Folder/'

#loop through multiple files
file_loop=[]
for root, dirs, find_files in os.walk(directory):
    for file in find_files:
        file_loop.append(os.path.join(root,file))

save_files=[]
for filename in file_loop:
    df=pd.read_csv(filename , sep = '|' , header = None, low_memory=False)
    df=df[[0,1,2,3,4,5,6,7,16,17]]
    df.columns=['Firm', 'MPID', 'Month', 'Ticker', 'Type',
               'Size', 'Orders', 'Shares', 'Avg_Profit', 'Avg_Client_Cost']
    df['Firm']=filename.split(directory)[1][0:4]
    df1=df[df.Type.isin([12,13])].copy()
    df1['Tot_Profit']= df1.Shares*df1.Avg_Profit
    save_files.append(df1)    
df=pd.concat(save_files)

#Aggregate the file to the Firm-Month-Stock
sums=df1.groupby(['Month','Ticker', 'Firm'])['Orders', 'Shares','Tot_Profit', 'Avg_Client_Cost'].sum()

#Getting variables in a dataframe and getting Mean, Std Dev, 50th, 10th & 90th percentile. 
stock=pd.DataFrame()
stock['num_of_trades']=sums['Orders']   #orders=number of trades
stock['avg_cost_retail_trades']=sums['Avg_Client_Cost']
stock['monthly_profit']=sums['Tot_Profit']  
stock['num_shares_traded']=sums['Shares']   #numbers of shares traded= shares
stock_stats=stock.describe(percentiles=[0.10, 0.90])

#Creating a dataframe for the number of stocks and getting Mean, Std Dev, 50th, 10th & 90th percentile. 
stock_number=pd.DataFrame()
stock_number['number_of_stock']=df.groupby(['Firm', 'Month']).Ticker.unique().apply(len)
number_of_stock_stat=stock_number.describe(percentiles=[0.10, 0.90])
print(stock_stats, number_of_stock_stat)



