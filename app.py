from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import os
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
    cur = mysql.connection.cursor()
    cur.execute("Select * from AAPL")
    results = cur.fetchall()
    title = 'stockapp'
    return render_template('base.html',title=title,stocklist=stocklist)

@app.route('/stock', methods=['POST'])
def stock():
    print(request.method)
    if request.method == 'POST':
        stock = request.form.get('stockname')
        
        cur = mysql.connection.cursor()
        cur.execute(f"Select * from {stock}")
        results = cur.fetchall()[0]

        return render_template('stock.html',stock = results)
    else:
        return render_template('stock.html',stock = '1')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)

