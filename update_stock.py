
# This src is for updating the stock
from alpha_vantage.timeseries import TimeSeries
import json, requests
import pandas as pd
import mysql.connector
import mysql
from sqlalchemy import create_engine
import json
# https://github.com/RomelTorres/alpha_vantage


# #################################################################
# Please modify the parameter of your mysql database
# #################################################################

api_key = '##########'
# Enter your api key from alpha_vantage here
# #################################################################

def update_stock(equity):
    ts = TimeSeries(key = api_key, output_format='pandas')
    data,meta_data = ts.get_daily_adjusted(symbol = equity, outputsize='full')
    rename = {'1. open':'open','2. high':'high','3. low':'low','4. close':'close','6. volume':'volume'}
    output = data.rename(columns=rename)
    output2 = output[['open','high','low','close','volume']]
    output3 = output.reset_index()
    output3 = output3[['date','open','high','low','close','volume']]
    # Get the attributes we need

    # Enter your personal mysql username and password
    # #################################################################
    engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
    # #################################################################
    con = engine.connect()
    output2.to_sql(equity, con=con, if_exists='replace', index = True)
    output3.to_csv(f'csv/{equity}.csv',header=False)
    con.close()

def update_index(index):
    ts = TimeSeries(key = api_key, output_format='pandas')
    data,meta_data = ts.get_daily_adjusted(symbol = index, outputsize='full')
    rename = {'1. open':'open','2. high':'high','3. low':'low','4. close':'close'}
    output = data.rename(columns=rename)
    output2 = output[['open','high','low','close']]
    # Get the attributes we need
    # #################################################################
    # Enter your personal mysql username and password
    engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
    # #################################################################
    con = engine.connect()
    output2.to_sql(index.replace(' ','_').replace('&',''), con=con, if_exists='replace', index = True)
    con.close()
    con.close()
