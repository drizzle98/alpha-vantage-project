import pandas as pd
import requests
import plotly
from plotly.offline import init_notebook_mode, iplot
import plotly.express as px
import plotly.graph_objs as go
import datetime
import json

def trace_plot(df):

    trace = go.Candlestick(x=df.date,
                       open=df.open,
                       high=df.high,
                       low=df.low,
                       close=df.close,
                       name = 'Candlestick')
    trace_close = go.Scatter(x=list(df.date),
                         y=list(df.close),
                         name='Close',line=dict(color='#71adf5'))
    trace_high = go.Scatter(x=list(df.date),
                        y=list(df.high),
                        visible = False,
                        name='High',
                        line=dict(color='#f2c270'))
    trace_low = go.Scatter(x=list(df.date),
                       y=list(df.low),
                       visible = False,
                       name='Low',
                       line=dict(color='#f28170'))

    data=[trace,trace_close,trace_high,trace_low]
    updatemenus = list([
        dict(type="buttons",
            active=99,
             x = 0.05,
             y = 0.99,
             bgcolor = '#a7bdde',#7d8ca3,#a7bdde
             bordercolor = '#FFFFFF',
             font = dict(color='white', size=12 ),#'#7d8ca3'
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
                             {'title': f'Close, High,and Low price of this ticker {df.name}'},
                 dict(label = 'Line',
                     method = 'update',
                     args = [{'visible': [True, True, True, True]},
                             {'title': f'Line of this ticker {df.name}'}])
                            ])
             ]))])
     # define the data and layout, and store them in the fig dictionary
    layout=go.Layout(title=f"{df.name}",autosize=True,updatemenus=updatemenus,
                     plot_bgcolor = '#ffe5e8')
    #I had to use offline.iplot in order to show this graph in notebook
    fig=dict(data=data,layout=layout)
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return plot_json

#df is a dataframe(date,stocka,stockb), a is name of stock a, b is name of stock b
def plot_line_compare(df,a,b):
    df=df.dropna()
    ######## fig 1 line Figure
    fig1 = px.line(df, x="date", y=[a,b],
                  hover_data={"date": "|%B %d, %Y"},
                  )
    fig1.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])))
    fig1.update_yaxes(autotypenumbers='convert types')
    fig1.update_layout(
        title={
            'text': "Two tickers' line comparison graph",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    line_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    return line_json



    ########  fig 2, area graph
def plot_area_compare(df,a,b):
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=df['date'], y=df[a],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(131, 90, 241)'),
        stackgroup='one', # define stack group
        name = a
    ))
    fig2.add_trace(go.Scatter(
        x=df['date'], y=df[b],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, color='rgb(111, 231, 219)'),
        stackgroup='one',
        name = b
    ))
    fig2.update_yaxes(autotypenumbers='convert types')
    fig2.update_layout(
        title={
            'text': "Two tickers' area comparison graph",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    area_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return area_json
