from flask import Flask, render_template, request, url_for, redirect, session,flash
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import validators, SubmitField, ValidationError
# from flask_bootstrap import Bootstrap
import pandas as pd
from sqlalchemy import create_engine
from plot import trace_plot
from update_stock import update_stock, update_index
import pandas as pd
from datetime import date, datetime

# import MySQL configuration

stocklist = ['MRNA', 'XOM', 'FPRX', 'FB', 'NFLX', 'MSFT', 'QS', 'TSLA', 'AAPL', 'AMZN', 'VUZI', 'HD', 'BABA', 'SQ', 'ZM', 'RIOT', 'GOOGL', 'NIO', 'NVDA', 'BA']
indexlist = ['S&P GSCI','S&P 500','NASDX']

app = Flask(__name__)
app.config['SECRET_KEY']='alpha_vantage'

class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format = '%Y-%m-%d',validators=(validators.Optional(),))
    enddate = DateField('End Date', format = '%Y-%m-%d',default=date.today(),validators=(validators.Optional(),))
    # def validate_startdate(form, field):
    #     print(form.startdate.data)
    #     print(form.enddate.data)
    #     if field.data > form.enddate.data:
    #         raise ValidationError('startdate must be earliere than enddate.')


@app.route('/',methods=['GET', 'POST'])
def base():
    _list = ['MRNA', 'XOM', 'FPRX',  'FB', 'NFLX', 'MSFT', 'QS', 'TSLA', 'AAPL', 'AMZN', 'VUZI', 'HD', 'BABA', 'SQ', 'ZM', 'RIOT', 'GOOGL', 'NIO', 'NVDA', 'BA','S&P GSCI','S&P 500','NASDX']
    title = 'stockapp'
    form = InfoForm()
    form2 = InfoForm()
    return render_template('base.html',title=title,stocklist=stocklist,indexlist=indexlist,_list=_list, form=form, form2=form2)


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


@app.route('/stock', methods=['GET','POST'])
def stock():
    if request.method == 'POST':
        qry= ''
        stock_name = request.form.get('stockname')
        check = request.form.getlist('check')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        for i in check:
            qry = qry + ',' + i
        if qry == '':
            qry = '*'
        else:
            qry = qry.lstrip(',')
        # Select all for the situation that none of them were checked.

        query1 = f"Select {qry} from {stock_name}"
        graph_query = f"select * from {stock_name}"
        if startdate != '':
            if startdate > enddate:
                start_date = enddate
                end_date = start_date
            else:
                start_date = startdate
                end_date = enddate
            subquery = f' where date >= "{start_date}" and date <= "{end_date}"'
        elif startdate == '':
            subquery = f' where date <= "{enddate}"'
        query = query1 + subquery
        g_query = graph_query + subquery

        
        #engine = create_engine("mysql+mysqlconnector://root:Jzx@1998@localhost/dsci551")
        engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")

        # Enter your personal mysql username and password
        #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        tables=df.to_html(classes=stock_name)

        df_graph = pd.read_sql_query(g_query,con)
        df_graph.rename(index=pd.to_datetime)
        df_graph.name=f'Price of {stock_name}'
        plot_json = trace_plot(df_graph)

        return render_template('stock.html',tables=tables, check=check,stockname=stock_name, plot_json=plot_json)
    else:
        return render_template('stock.html',stockname= 'Invalid')




@app.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':
        qry= ''
        index_name = request.form.get('indexname')
        index_new = index_name.replace(' ','_').replace('&','')
        check = request.form.getlist('check2')
        startdate = request.form.get('startdate')
        enddate = request.form.get('enddate')
        for i in check:
            qry = qry + ',' + i
        if qry == '':
            qry = '*'
        else:
            qry = qry.lstrip(',')
        # Select all for the situation that none of them were checked.
        query1 = f"Select {qry} from {index_new}"
        graph_query = f"select * from {index_new}"
        if startdate != '':
            if startdate > enddate:
                start_date = enddate
                end_date = start_date
            else:
                start_date = startdate
                end_date = enddate
            subquery = f' where date >= "{start_date}" and date <= "{end_date}"'
        elif startdate == '':
            subquery = f' where date <= "{enddate}"'
        query = query1 + subquery
        g_query = graph_query + subquery

        #engine = create_engine("mysql+mysqlconnector://root:Jzx@1998@localhost/dsci551")
        engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")
        # Enter your personal mysql username and password
        #  engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        tables=df.to_html(classes=index_new)


        df_graph = pd.read_sql_query(g_query,con)
        df_graph.rename(index=pd.to_datetime)
        df_graph.name=f'Price of {index_name}'
        plot_json = trace_plot(df_graph)

        return render_template('stock.html',tables=tables, check=check,index_name=index_name, plot_json=plot_json)
    else:
        return render_template('stock.html',index_name = 'Invalid')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)
