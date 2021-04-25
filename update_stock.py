
# This src is for updating the stock
from alpha_vantage.timeseries import TimeSeries
import json, requests
import pandas as pd
import mysql.connector
import mysql
from sqlalchemy import create_engine
# https://github.com/RomelTorres/alpha_vantage

api_key = '6H0W9Q4RDDBVU43C'
# api_key = '##########'
# Enter your api key from alpha_vantage here

def update_stock(equity):
    ts = TimeSeries(key = api_key, output_format='pandas')
    data,meta_data = ts.get_intraday(symbol = equity, interval = '1min', outputsize='full')
    rename = {'1. open':'Open','2. high':'High','3. low':'Low','4. close':'Close','5. volume':'Volume'}
    output = data.rename(columns=rename)
    engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")
    # Enter your personal mysql username and password
    #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")

    con = engine.connect()
    output.to_sql(equity, con=con, if_exists='replace', index = True)
    con.close()

def update_index(index):
    ts = TimeSeries(key = api_key, output_format='pandas')
    data,meta_data = ts.get_daily_adjusted(symbol = index, outputsize='full')
    rename = {'1. open':'Open','2. high':'High','3. low':'Low','4. close':'Close'}
    output = data.rename(columns=rename)
    output2 = output[['Open','High','Low','Close']]
    # Get the attributes we need
    engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")
    # Enter your personal mysql username and password
    #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
    con = engine.connect()
    output2.to_sql(index.replace(' ','_').replace('&',''), con=con, if_exists='replace', index = True)
    con.close()
