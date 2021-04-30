from flask import Flask, render_template, request, url_for, redirect, session,flash
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import validators, SubmitField, ValidationError
from flask_bootstrap import Bootstrap
import pandas as pd
from sqlalchemy import create_engine
from plot import trace_plot, plot_line_compare, plot_area_compare
from update_stock import update_stock, update_index
import pandas as pd
from datetime import date, datetime

import findspark
# findspark.init()

# Find spark automatically to avoid further error.import pyspark
# Comment this if the system can find pyspark automatically.
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import Row

# #################
# #################
# #################
# Please modify mysql engine parameter in function stock and index 
# #################
# #################
# #################

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
                return render_template('update.html',alert = 'Updated successfully',stockname=stockname)
            except:
                return render_template('update.html',alert = 'Failed to update',stockname=stockname)
        elif stockname in indexlist:
            try:
                update_index(stockname)
                return render_template('update.html',alert = 'Updated successfully',stockname=stockname)
            except:
                return render_template('update.html',alert = 'Failed to update',stockname=stockname)
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

        # Enter your personal mysql username and password
        # #################################################################
        engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        # #################################################################
        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        tables=df.to_html(classes='table table-striped tbs',justify='center')

        df_graph = pd.read_sql_query(g_query,con)
        df_graph.rename(index=pd.to_datetime)
        df_graph.name=f'Price of {stock_name}'
        plot_json = trace_plot(df_graph)

        return render_template('stock.html',tables=tables, check=check,stockname=stock_name, plot_json=plot_json)
    else:
        return render_template('stock.html',stockname= 'Invalid')

@app.route('/tickers', methods=['POST','GET'])
def tickers():
    return render_template('tickers.html')



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


        # Enter your personal mysql username and password
        # #################################################################
        engine = create_engine("mysql+mysqlconnector://usrname:pwd@host/database")
        # #################################################################

        con = engine.connect()
        # Create mySql connection
        df = pd.read_sql_query(query,con)
        tables=df.to_html(classes='table table-striped tbs',justify='center')


        df_graph = pd.read_sql_query(g_query,con)
        df_graph.rename(index=pd.to_datetime)
        df_graph.name=f'Price of {index_name}'
        plot_json = trace_plot(df_graph)

        return render_template('stock.html',tables=tables, check=check,index_name=index_name, plot_json=plot_json)
    else:
        return render_template('stock.html',index_name = 'Invalid')


@app.route('/compare', methods=['POST'])
def compare():
    if request.method == 'POST':
        tickers = request.form.getlist('compare')

    ticker1 = tickers[0]
    ticker2 = tickers[1]

    spark = SparkSession.builder.appName('alpha_vantage').getOrCreate()
    t1 = spark.read.csv(f'csv/{ticker1}.csv')
    t2 = spark.read.csv(f'csv/{ticker2}.csv')
    rdd1 = t1.rdd
    rdd2 = t2.rdd

    rdd_1 = rdd1.map(lambda x: (x['_c1'],x['_c5']))
    rdd_2 = rdd2.map(lambda x: (x['_c1'],x['_c5']))
    temp = rdd_1.join(rdd_2)

    temp2 = temp.map(lambda x: (x[0],x[1][0],x[1][1]))
# final = spark.sparkContext.parallelize(temp2.collect())
# df = final.toPandas()
    sparkDF = temp2.map(lambda x: str(x)).map(lambda w: w.replace('(','').replace(')','').replace("'",'').split(',')).toDF()
    pd_final = sparkDF.toPandas()
    rename2 = {'_1':'date','_2':ticker1,'_3':ticker2}
    pd_final = pd_final.rename(columns=rename2)
    pd_final.sort_values(by=['date'], inplace=True, ascending=False)
    pd_table = pd_final.reset_index(drop=True) 
    tables=pd_table.to_html(classes='table table-striped tbs',justify='center')
    line_json=plot_line_compare(pd_final,ticker1,ticker2)
    # area_json=plot_area_compare(pd_final,ticker1,ticker2)

    return render_template('compare.html', tables=tables,line_json=line_json)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)
