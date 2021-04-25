import pandas as pd 
import os, json

for file in os.listdir('csv'):
    data = pd.read_csv('csv/'+file,encoding='utf-8')
    rename = {'1. open':'Open','2. high':'High','3. low':'Low','4. close':'Close','5. volume':'Volume'}
    output = data.rename(columns=rename)
    output.to_csv('csv/'+file)
