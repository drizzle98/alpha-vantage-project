import pandas as pd
import requests
import plotly 
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import datetime
import json

def trace_plot(df):
    # init_notebook_mode()
    trace = go.Candlestick(x=df.index,
                       open=df.Open,
                       high=df.High,
                       low=df.Low,
                       close=df.Close,
                       name = 'Candlestick')
    trace_close = go.Scatter(x=list(df.index),
                         y=list(df.Close),
                         name='Close',line=dict(color='#71adf5'))
    trace_high = go.Scatter(x=list(df.index),
                        y=list(df.High),
                        visible = False,
                        name='High',
                        line=dict(color='#f2c270'))
    trace_low = go.Scatter(x=list(df.index),
                       y=list(df.Low),
                       visible = False,
                       name='Low',
                       line=dict(color='#f28170'))
    
    data=[trace,trace_close,trace_high,trace_low]
    updatemenus = list([
        dict(type="buttons",
            active=99,
             x = 0.05,
             y = 0.99,
             bgcolor = '#a7bdde',
             bordercolor = '#FFFFFF',
             font = dict( color='#7d8ca3', size=11 ),
             direction = 'left',
             xanchor = 'left',
             yanchor = 'top',
             buttons=list([
                 dict(label = 'Candlestick',
                     method = 'update',
                     args = [{'visible': [True, False, False, False]},
                             {'title': f'Candlestick of this ticker {df.name}'}]),
                 dict(label = 'Close-High-Low',
                     method = 'update',
                     args = [{'visible': [False, True, True, True]},
                             {'title': f'Close, High,and Low price of this ticker {df.name}'}
                            ])
             ]))])
     # define the data and layout, and store them in the fig dictionary                        
    layout=go.Layout(title=f"{df.name}",autosize=True,updatemenus=updatemenus,
                     plot_bgcolor = '#ffe5e8')
    #I had to use offline.iplot in order to show this graph in notebook
    fig=dict(data=data,layout=layout)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return plot_json