#!/usr/bin/env python
# coding: utf-8

# In[32]:


import pandas as pd
import requests
import plotly 
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
import plotly.graph_objs as go
import datetime as dt
import json


import plotly.express as px
import plotly.graph_objects as go


# In[60]:


AAPL=pd.read_json(open("json/AAPL.json",'r'))
AAPL
AMZN=pd.read_json(open("json/AMZN.json",'r'))
AMZN
d=AAPL.merge(AMZN,on='date',how='left')
# AAPL=pd.Dataframe.from_dict(AAPL)
# area_chart = px.area(stocks_close.FB, title = 'FACEBOOK SHARE PRICE (2013-2020)')

# area_chart.update_xaxes(title_text = 'Date')
# area_chart.update_yaxes(title_text = 'FB Close Price', tickprefix = '$')
# area_chart.update_layout(showlegend = False)


# area_chart.show()
f=d[['date','1. open_x','1. open_y']].dropna()
f['AAPL']=f['1. open_x']
f['AMZN']=f['1. open_y']

f.set_index('date')[['AAPL','AMZN']].plot()


# In[ ]:


f.set_index('date')[['AAPL','AMZN']].plot()


# In[61]:


import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=a, y=f['Date'], fill='tozeroy'))
fig.show()


# In[ ]:




