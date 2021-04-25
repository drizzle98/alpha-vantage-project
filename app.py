from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
from sqlalchemy import create_engine
import os
from plot import trace_plot
from update_stock import update_stock, update_index
import pandas as pd


# import MySQL configuration

stocklist = ['MRNA', 'XOM', 'FPRX', 'FB', 'NFLX', 'MSFT', 'QS', 'TSLA', 'AAPL', 'AMZN', 'VUZI', 'HD', 'BABA', 'SQ', 'ZM', 'RIOT', 'GOOGL', 'NIO', 'NVDA', 'BA']
indexlist = ['S&P GSCI','S&P 500','NASDX']

app = Flask(__name__)

# mysql = MySQL(app)
@app.route('/')

def base():
    _list = ['MRNA', 'XOM', 'FPRX',  'FB', 'NFLX', 'MSFT', 'QS', 'TSLA', 'AAPL', 'AMZN', 'VUZI', 'HD', 'BABA', 'SQ', 'ZM', 'RIOT', 'GOOGL', 'NIO', 'NVDA', 'BA','S&P GSCI','S&P 500','NASDX']
    title = 'stockapp'

    return render_template('base.html',title=title,stocklist=stocklist,indexlist=indexlist,_list=_list)


@app.route('/update', methods=['POST'])
def update():
    # This part is for the streaming. One stock can be updated at a time due to the API limit.
    if request.method == 'POST':
        stockname = request.form.get('_list')
        if stockname in stocklist:
            try:
                update_stock(stockname)
                return render_template('update.html',alert = 'Update successfully',stockname=stockname)
            except:
                return render_template('update.html',alert = 'Fail to update',stockname=stockname)
        elif stockname in indexlist:
            try:
                update_index(stockname)
                return render_template('update.html',alert = 'Update successfully',stockname=stockname)
            except:
                return render_template('update.html',alert = 'Fail to update',stockname=stockname)
    else:
        return render_template('update.html',alert = 'Fail to update')


@app.route('/stock', methods=['POST'])
def stock():
    if request.method == 'POST':
        qry= ''
        stock_name = request.form.get('stockname')
        check = request.form.getlist('check')
        for i in check:
            qry = qry + ',' + i
        if qry == '':
            qry = '*'
        else:
            qry = qry.lstrip(',')
        # Select all for the situation that none of them were checked.

        query = f"Select {qry} from {stock_name}"
        #engine = create_engine("mysql+mysqlconnector://root:Jzx@1998@localhost/dsci551")
        engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")

        # Enter your personal mysql username and password
        #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        df2 = pd.read_sql_query(f'select * from {stock_name}',con)
        tables=df.to_html(classes=stock_name)


        df2.rename(index=pd.to_datetime)
        df2.name=f'Price of {stock_name}'
        plot_json = trace_plot(df2)

        return render_template('stock.html',tables=tables, check=check,stockname=stock_name, plot_json=plot_json)
    else:
        return render_template('stock.html',stock = '1')




@app.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':
        qry= ''
        index_name = request.form.get('indexname')
        index_new = index_name.replace(' ','_').replace('&','')
        check = request.form.getlist('check2')
        for i in check:
            qry = qry + ',' + i
        if qry == '':
            qry = '*'
        else:
            qry = qry.lstrip(',')
        # Select all for the situation that none of them were checked.

        query = f"Select {qry} from {index_new}"
        #engine = create_engine("mysql+mysqlconnector://root:Jzx@1998@localhost/dsci551")

        engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")
        # Enter your personal mysql username and password
        #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        df2 = pd.read_sql_query(f'select * from {index_new}',con)
        tables=df.to_html(classes=index_new)


        df2.rename(index=pd.to_datetime)
        df2.name=index_name
        plot_json = trace_plot(df2)

        return render_template('stock.html',tables=tables, check=check,index_name=index_name, plot_json=plot_json)
    else:
        return render_template('stock.html',stock = '1')







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)
