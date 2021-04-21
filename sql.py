import mysql.connector
import os
import json

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'wxy110218',
    database = 'stockapp'
    )

mycursor = db.cursor()

# mycursor.execute("CREATE DATABASE dsci551")
# # Create database
def create_db(db_name,style):
    mycursor.execute(f"DROP TABLE IF EXISTS {db_name};")
    if style == 1:
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {db_name} (date TIMESTAMP, open double, high double, low double, close double, volume double);")
    if style == 2:
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {db_name} (date DATETIME, open double, high double, low double, close double, ad_close double, volume double, divident double);")


for file in os.listdir('json'):
    filename = file.replace('.json','').replace(' ','_').replace('&','')
    json_data = json.loads(open('json/'+file).read())
    if 'index' in filename:
        create_db(filename,2)
        for i in json_data:
            date = i['date']
            open_p = i['1. open']
            high = i['2. high']
            low = i['3. low']
            close_p = i['4. close']
            ad_close = i['5. adjusted close']
            volume = i['6. volume']
            divi = i['7. dividend amount']
            content = f'"{date}",{open_p},{high},{low},{close_p},{ad_close},{volume},{divi}'
            mycursor.execute(f"INSERT INTO {filename} (date,open,high,low,close,ad_close,volume,divident) VALUES ({content})")

    else:
        create_db(filename,1)
        for i in json_data:
            date = i['date']
            open_p = i['1. open']
            high = i['2. high']
            low = i['3. low']
            close_p = i['4. close']
            volume = i['5. volume']
            content = f'"{date}",{open_p},{high},{low},{close_p},{volume}'
            mycursor.execute(f"INSERT INTO {filename} (date,open,high,low,close,volume) VALUES ({content})")
    db.commit()

db.close()

