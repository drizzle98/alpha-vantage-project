import findspark
findspark.init()
# Find spark automatically to avoid further error.import pyspark
# Comment this if the system can find pyspark automatically.
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import Row
import pandas as pd
from sqlalchemy import create_engine
from alpha_vantage.timeseries import TimeSeries
import json

# engine = create_engine("mysql+mysqlconnector://root:wxy110218@localhost/stockapp")

# con = engine.connect()
spark = SparkSession.builder.appName('alpha_vantage').getOrCreate()
fb = spark.read.csv('csv/FB.csv')
qs = spark.read.csv('csv/QS.csv')
rdd1 = fb.rdd
rdd2=qs.rdd

# print(rdd1.take(2))
rdd_1 = rdd1.map(lambda x: (x['_c1'],x['_c5']))
rdd_2 = rdd2.map(lambda x: (x['_c1'],x['_c5']))
temp = rdd_1.join(rdd_2)

temp2 = temp.map(lambda x: (x[0],x[1][0],x[1][1]))
# final = spark.sparkContext.parallelize(temp2.collect())
# df = final.toPandas()
sparkDF = temp2.map(lambda x: str(x)).map(lambda w: w.split(',')).toDF()
pd_final = sparkDF.toPandas()
rename2 = {'_1':'date','_2':'FB','_3':'QS'}
pd_final = pd_final.rename(columns=rename2)
print(pd_final)
# query='select * from FB'
# df = pd.read_sql_query(query,con)
# s_df = spark.createDataFrame(df)
# s_df_rdd = s_df.rdd

# def f(x):
#     d = {}
#     for i in range(len(x)):
#         d[str(i)] = x[i]
#     return d

# #Now populate that
# df2 = s_df_rdd.map(lambda x: Row(**f(x))).toDF()
# print(df2.columns)
# print(df2.show())
# api_key = 'ZHJ3NVHS79RER2KZ'

# ts = TimeSeries(key = api_key, output_format='pandas')
# data,meta_data = ts.get_daily_adjusted(symbol = 'FB', outputsize='full')
# rename = {'1. open':'open','2. high':'high','3. low':'low','4. close':'close','6. volume':'volume'}
# output = data.rename(columns=rename)
# output = output[['date','open','high','low','close','volume']]
# output.to_csv('csv/FB.csv')

# print(output)
