# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:16:53 2023

@author: rwenzel
"""
import platform

import StockHero as stock
import yfinance as yf

import streamlit as st
from plotly import graph_objs as go
from prophet.plot import plot_plotly

from prophet import Prophet

if platform.system() == "Windows":
    import win32clipboard as clipboard
else:
    import pyperclip as clipboard

#import plotly.io as io
#io.renderers.default='browser'
#import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

    #########################
    ###                   ###
    ###    Morningstar    ###
    ###     functions     ###
    ###                   ###
    #########################

@st.cache_data
def get_data_morningstar(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.morningstar.key_statistics
    try:
        name = ticker.morningstar.name_id
    except:
        name = "Das ist kein gültiger Name !"
    data_load_state.text("Loading data...done!")
    return data, name

    #########################
    ###                   ###
    ###    Meta Forecast  ###
    ###     functions     ###
    ###                   ###
    #########################

@st.cache_data
def load_data(ticker, START, TODAY):
    data_load_state = st.text("Load data...")
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    data_load_state.text("Loading data...done!")
    return data

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'], name = 'stock_close'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible = True)
    st.plotly_chart(fig)
    
def plot_forecast(m, forecast):
    fig = plot_plotly(m, forecast)
    
    fig.data[0].marker.color = 'blue'
    fig.data[0].line.color = 'blue'
    
    fig.data[2].marker.color = 'red'
    fig.data[2].line.color = 'red'
    
    fig.update_layout(title_text = "Forecast data")
    st.plotly_chart(fig)
    
def prediction(df_train, period):
    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    return m, forecast

    #########################
    ###                   ###
    ###     Gurufocus     ###
    ###     functions     ###
    ###                   ###
    #########################

@st.cache_data
def get_data_gurufocus_pe(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.gurufocus.pe_ratio_av
    data_load_state.text("Loading data...done!")
    return data

@st.cache_data
def get_data_gurufocus_debt_to_ebitda(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.gurufocus.debt_to_ebitda
    data_load_state.text("Loading data...done!")
    return data

@st.cache_data
def get_data_gurufocus_div_yield(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.gurufocus.div_yield_av
    data_load_state.text("Loading data...done!")
    return data

    ##########################
    ###                    ###
    ###    Stratosphere    ###
    ###     functions      ###
    ###                    ###
    ##########################

@st.cache_resource
def get_data_stratosphere_returns(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.stratosphere.returns
    data_load_state.text("Loading data...done!")
    return data

@st.cache_resource
def get_data_stratosphere_margins(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    data = ticker.stratosphere.margins
    data_load_state.text("Loading data...done!")
    return data

    #####################
    ###               ###
    ###    General    ###
    ###   functions   ###
    ###               ###
    #####################

def set_clipboard_text(text):
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardText(text)
    clipboard.CloseClipboard()

    #####################
    ###               ###
    ###      CNN      ###
    ###   functions   ###
    ###               ###
    #####################

def cnn_fear_and_greed():
    exchange = stock.StockExchange('CNN')
    json = exchange.cnn_fear_and_greed_graph_data
    
    # Extracting data from JSON
    x_values = [json['market_momentum_sp500']['data'][i]['x'] for i in range(len(json['market_momentum_sp500']['data']))]
    y_values = [json['market_momentum_sp500']['data'][i]['y'] for i in range(len(json['market_momentum_sp500']['data']))]

    #x2_values = [json['market_momentum_sp125']['data'][i]['x'] for i in range(len(json['market_momentum_sp125']['data']))]
    y2_values = [json['market_momentum_sp125']['data'][i]['y'] for i in range(len(json['market_momentum_sp125']['data']))]

    # Converting Unix epoch time to datetime objects
    x_datetime = [datetime.fromtimestamp(x / 1000) for x in x_values]
    #x2_datetime = [datetime.fromtimestamp(x / 1000) for x in x2_values]
    timestamp = datetime.fromtimestamp(json['market_momentum_sp500']['timestamp'] / 1000)
    timestamp_formatted = timestamp.strftime('%a %b %d %Y %H:%M:%S GMT%z')

    # Convert data to Pandas DataFrame
    data = {'Date': x_datetime, 'Momentum': y_values, 'Moving Average': y2_values}
    df = pd.DataFrame(data)

    # Creating an interactive Plotly chart
    fig = go.Figure()

    # Adding the S&P 500 Momentum line
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Momentum'], mode='lines', name='S&P 500', line=dict(color='#1f77b4')))

    # Adding the 125-day Moving Average line
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Moving Average'], mode='lines', name='125-day Moving Average', line=dict(color='#ff7f0e')))

    # Adding the rating annotation
    rating = json['market_momentum_sp500']['rating'].upper()
    fig.add_annotation(
        text=rating,
        x=1,
        y=1.08,
        xref='paper',
        yref='paper',
        showarrow=False,
        font=dict(size=25, color='red'),
        align='right',
        xanchor='right',
        yanchor='top',
        bordercolor='black',  # Border color
        borderwidth=1,        # Border width
        borderpad=5          # Border padding
    )

    # Adding titles and labels
    fig.update_layout(
        title='<span style="font-size:24px;"><b>Market Momentum</b></span><br><br>S&P 500 and its 125-day moving average',
        #xaxis_title = timestamp_formatted,
        xaxis=dict(gridcolor='lightgrey', 
                   showgrid=True
                   ),  # Set grid color for x-axis
        yaxis=dict(
                    gridcolor='lightgrey', 
                    side='right',
                    tickformat=',.2f',
                    tickfont=dict(size=15)
                    ),  # Set grid color for y-axis
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        legend=dict(x=0.04, y=0.95), 
        legend_orientation='h',
        shapes=[
        # Adding a line shape to mimic the x-axis
        dict(
            type="line",
            x0=min(x_values),  # Starting x-coordinate of the line
            x1=max(x_values),  # Ending x-coordinate of the line
            y0=min(y_values) - 50.0,  # y-coordinate of the line (adjust as needed)
            y1=min(y_values) - 50.0,  # y-coordinate of the line (adjust as needed)
            line=dict(color="black", width=2)
        )
        ]
    )

    # Add a text annotation to simulate the x-axis title at the desired position
    fig.add_annotation(
        text=timestamp_formatted,
        x=1.04,  # Set the x-coordinate to position the text to the right
        y=-0.1,  # Adjust the y-coordinate to control the vertical position
        xref='paper',
        yref='paper',
        showarrow=False,
        font=dict(size=14, color='white'),  # Adjust the font properties as needed
        align='right',
    )

    # Show the interactive chart
    fig.update_layout(height=600, width=1400)
    st.plotly_chart(fig)

@st.cache_data
def eqs_news(ticker):
    ticker = stock.Ticker(ticker)
    data_load_state = st.text("Load data...")
    t = stock.StockExchange('something')
    data = t.eqs_news_latest_news(10, 'Stabilus')
    data_load_state.text("Loading data...done!")
    return data