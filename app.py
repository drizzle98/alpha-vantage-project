from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import os
from plot import trace_plot
import pandas as pd
# import MySQL configuration


app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'wxy110218'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'stockapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
@app.route('/')

def index():
    stocklist = ['MRNA', 'XOM', 'FPRX', 'NASDX_index', 'FB', 'SP_GSCI_index', 'NFLX', 'MSFT', 'QS', 'TSLA', 'AAPL', 'AMZN', 'VUZI', 'HD', 'BABA', 'SQ', 'ZM', 'RIOT', 'GOOGL', 'NIO', 'SP_500_index', 'NVDA', 'BA']
    title = 'stockapp'
    return render_template('base.html',title=title,stocklist=stocklist)

@app.route('/stock', methods=['POST'])
def stock():
    if request.method == 'POST':
        qry= ''
        stock = request.form.get('stockname')
        check = request.form.getlist('check')
        for i in check:
            qry = qry + ',' + i
        qry = qry.lstrip(',')
        cur = mysql.connection.cursor()
        query = f"Select {qry} from {stock}"

        cur.execute(query)
        results = cur.fetchall()[0]



        TSLA=pd.read_csv("csv/TSLA.csv",index_col=0)
        TSLA.rename(index=pd.to_datetime)
        TSLA.name='特斯拉股价'
        plot_json = trace_plot(TSLA)
        print(plot_json)
    # Test for embedding picture



        return render_template('stock.html',stock = results, check=check, plot_json=plot_json)
    else:
        return render_template('stock.html',stock = '1')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)
