# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:02:58 2023

@author: rwenzel
"""

from Funktionen.functions import get_data_morningstar
from Funktionen.functions import load_data
from Funktionen.functions import plot_raw_data
from Funktionen.functions import plot_forecast
from Funktionen.functions import prediction

import streamlit as st
import win32clipboard

from datetime import date

class GUI:
    def __init__(self):    
        st.sidebar.title('Options')
        option = st.sidebar.selectbox("Which Dashboard?", ('Forecasting', 'Morningstar'), 0)
        #st.header(option)
        
        if option == 'Morningstar':
            morningstar_gui()
            
        if option == 'Forecasting':
            prophet_gui()

def morningstar_gui():
        st.title('Ticker-Symbol Eingabe')
        
        # Eingabebox für das Ticker-Symbol
        ticker_symbol = st.text_input('Gib das Ticker-Symbol ein:')
        
        # Zeige das eingegebene Ticker-Symbol an
        if ticker_symbol:
            st.write(f'Du hast das Ticker-Symbol eingegeben: {ticker_symbol}')

        # Button, um den DataFrame zu kopieren
        if st.button('DataFrame kopieren'):
            df = get_data_morningstar(ticker_symbol)
            df_markdown = df.to_markdown()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(df_markdown)
            win32clipboard.CloseClipboard()
            st.write('DataFrame wurde in die Zwischenablage kopiert.')
            st.write(df)

def prophet_gui():
        START = "2015-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")

        st.title("Stock Prediction")

        selected_stock = st.text_input("Gib das Ticker-Symbol ein:", "AAPL")

        n_years = st.slider("Years of prediction:", 1, 4)
        period = n_years * 365
        
        data = load_data(selected_stock, START, TODAY)
        
        plot_raw_data(data)
        
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns = {"Date": "ds", "Close": "y"})
        
        m, forecast = prediction(df_train, period)
        
        plot_forecast(m, forecast)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        