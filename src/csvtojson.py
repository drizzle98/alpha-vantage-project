import pandas as pd 
import os, json

for file in os.listdir('csv'):
    filename = file.replace('.csv','.json')

    data = pd.read_csv(file,encoding='utf-8')
    jdata = data.to_dict(orient='records')
    with open(f'json/{filename}','w') as f:
        json.dump(jdata,f)