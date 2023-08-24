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

def set_clipboard_text(text):
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardText(text)
    clipboard.CloseClipboard()