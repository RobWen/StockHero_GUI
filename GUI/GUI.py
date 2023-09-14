# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:02:58 2023

@author: rwenzel
"""

from Funktionen.functions import *

import streamlit as st

from datetime import date

class GUI:
    def __init__(self):
        st.set_page_config(page_title="StockHero",layout="wide")
        st.sidebar.title('Options')
        option = st.sidebar.selectbox("Which Dashboard?", ('Forecasting', 'Morningstar', 'Gurufocus', 'Stratosphere', 'CNN'), 4)
        
        if option == 'Forecasting':
            self.prophet_gui()

        if option == 'Morningstar':
            self.morningstar_gui()

        if option == 'Gurufocus':
            self.gurufocus_gui()
            
        if option == 'Stratosphere':
            self.stratosphere_gui()
            
        if option == 'CNN':
            self.cnn_gui()

    ################################
    ###                          ###
    ###       Prophet GUI        ###
    ###                          ###
    ################################

    def prophet_gui(self):
        START = "2013-01-01"
        TODAY = date.today().strftime("%Y-%m-%d")
    
        st.title("Stock Prediction")
    
        # Creating two columns:
        left_col, right_col = st.columns([3, 1])
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            selected_stock = st.text_input("Gib das Ticker-Symbol ein:")
    
            if selected_stock:
                n_years = st.slider("Years of prediction:", 1, 4)
                period = n_years * 365
                
                data = load_data(selected_stock, START, TODAY)
                
                plot_raw_data(data)
                
                df_train = data[['Date', 'Close']]
                df_train = df_train.rename(columns = {"Date": "ds", "Close": "y"})
                
                m, forecast = prediction(df_train, period)
                
                plot_forecast(m, forecast)

    ################################
    ###                          ###
    ###     Morningstar GUI      ###
    ###                          ###
    ################################

    def morningstar_gui(self):
        st.title('Eingabe')
        
        # Creating two columns:
        left_col, right_col = st.columns([5,4])
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            ticker_symbol = st.text_input('Gib das Ticker-Symbol / die ISIN / den Namen ein:')
            df, name_symbol = get_data_morningstar(ticker_symbol)
        
        # Zeige das eingegebene Ticker-Symbol an
        if ticker_symbol:
            with right_col:
                st.write("Du hast folgendes Unternehmen eingegeben:")
                centered_text = f"<div style='text-align: left; font-size: 24px;'>{name_symbol}</div>"
                st.write(f'{centered_text}', unsafe_allow_html=True)
    
        # Button, um den DataFrame zu kopieren
        if st.button('DataFrame kopieren'):
            df, name = get_data_morningstar(ticker_symbol)
            if df is not None: 
                df_markdown = df.to_markdown()
                set_clipboard_text(df_markdown)
                st.write('DataFrame wurde in die Zwischenablage kopiert.')
                st.write(df)
            else:
                st.write(':sunglasses:')

    ################################
    ###                          ###
    ###       Gurufocus GUI      ###
    ###                          ###
    ################################
        
    def gurufocus_gui(self):    
        st.title('Ticker-Symbol Eingabe')
        
        # Creating two columns:
        left_col, right_col = st.columns(2)
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            ticker_symbol = st.text_input('Gib das Ticker-Symbol ein:')
        
        # Zeige das eingegebene Ticker-Symbol an
        with right_col:
            if ticker_symbol:
                st.write(f'Du hast das Ticker-Symbol eingegeben: {ticker_symbol}')
        
        # Button, um den DataFrame zu kopieren
        with left_col:
            if st.button('Historisches PE-Ratio'):
                df = get_data_gurufocus_pe(ticker_symbol)
                df_markdown = df.to_markdown()
                set_clipboard_text(df_markdown)
                st.write('DataFrame wurde in die Zwischenablage kopiert.')
                with right_col:
                    st.write(df)
            
        # Button, um den DataFrame zu kopieren
        with left_col:
            if st.button('Historisches Debt-to-EBITDA-Ratio'):
                df = get_data_gurufocus_debt_to_ebitda(ticker_symbol)
                if df is None:
                    with right_col:
                        st.markdown("<font color='green'>Debt-to-EBITDA is not ranked, so likely no debt</font>", unsafe_allow_html=True)
                else:
                    df_markdown = df.to_markdown()
                    set_clipboard_text(df_markdown)
                    st.write('DataFrame wurde in die Zwischenablage kopiert.')
                    with right_col:
                        st.write(df)
        
        # Button, um den DataFrame zu kopieren
        with left_col:
            if st.button('Historische Dividenden-Rendite'):
                df = get_data_gurufocus_div_yield(ticker_symbol)
                df_markdown = df.to_markdown()
                set_clipboard_text(df_markdown)
                st.write('DataFrame wurde in die Zwischenablage kopiert.')
                with right_col:
                    st.write(df)
        
    ################################
    ###                          ###
    ###    Stratosphere GUI      ###
    ###                          ###
    ################################
    
    def stratosphere_gui(self):
        st.title('Eingabe')
        
        # Creating two columns:
        left_col, right_col = st.columns(2)
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            ticker_symbol = st.text_input('Gib das Ticker-Symbol ein:')
              
        # Zeige das eingegebene Ticker-Symbol an
        with right_col:
            if ticker_symbol:
                st.write(f'Du hast das Ticker-Symbol eingegeben: {ticker_symbol}')
            
        # Button, um den DataFrame zu kopieren
        with left_col:
            if st.button('Returns (5Y Avg)'):
                df = get_data_stratosphere_returns(ticker_symbol)
                df_markdown = df.to_markdown()
                set_clipboard_text(df_markdown)
                st.write('DataFrame wurde in die Zwischenablage kopiert.')
                with right_col:
                    st.write(df)
        
        # Button, um den DataFrame zu kopieren
        with left_col:
            if st.button('Margins'):
                df = get_data_stratosphere_margins(ticker_symbol)
                df_markdown = df.to_markdown()
                set_clipboard_text(df_markdown)
                st.write('DataFrame wurde in die Zwischenablage kopiert.')
                with right_col:
                    st.write(df)
        
    ################################
    ###                          ###
    ###     Morningstar GUI      ###
    ###                          ###
    ################################
        
    def cnn_gui(self):
        cnn_fear_and_greed()
        