import pandas as pd
import requests
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json

#read data and join data
def plot_compare(df,ticker1,ticker2):

#first fig, one graph with two lines
    fig1 = px.line(df, x="date", y=[ticker1,ticker2],
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
    fig1.update_layout(
    title={
        'text': "Two tickers' line comparison graph",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig1.show()


    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
    x=df['date'], y=df[ticker1],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(131, 90, 241)'),
    stackgroup='one' # define stack group
        ))
    fig2.add_trace(go.Scatter(
    x=df['date'], y=df[ticker2],
    hoverinfo='x+y',
    mode='lines',
    line=dict(width=0.5, color='rgb(111, 231, 219)'),
    stackgroup='one'
    ))
    fig2.update_layout(
    title={
        'text': "Two tickers' area comparison graph",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig2.show()
