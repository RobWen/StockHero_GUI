# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:02:58 2023

@author: rwenzel
"""

from Funktionen.functions import *

import streamlit as st

from datetime import date, timedelta

class GUI:
    def __init__(self):
        st.set_page_config(page_title="StockHero",layout="wide")
        st.sidebar.title('Options')
        option = st.sidebar.selectbox("Which Dashboard?", ('Forecasting', 'Morningstar', 'Gurufocus', 
                                                           'Stratosphere', 'CNN', 'Stock Dashboard'), 4)
        
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
            
        if option == 'Stock Dashboard':
            self.stock_dashboard_gui()

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
        
    ########################
    ###                  ###
    ###     CNN GUI      ###
    ###                  ###
    ########################
        
    def cnn_gui(self):
        cnn_fear_and_greed()
        
    ########################
    ###                  ###
    ###     Stock        ###
    ###   Dashboard      ###
    ###                  ###
    ########################
    
    def stock_dashboard_gui(self):
    
        st.title('Stock Dashboard')
        
        ticker = st.sidebar.text_input('Ticker', value='STM.DE')
        default_date = date(2022, 1, 1)
        start_date = st.sidebar.date_input('Start Date', value=default_date)
        end_date = st.sidebar.date_input('End Date')
    
        # Creating two columns:
        left_col, right_col = st.columns([3, 1])
        
        with right_col:
            
            if st.checkbox('Checkbox'):
                st.balloons()
    
        import yfinance as yf
        
        data = yf.download(ticker, start = start_date, end = end_date)
    
        #data = load_data(ticker, start_date, end_date)
        
        #plot_raw_data(data)
        
        import plotly.express as px
        
        fig = px.line(data, x = data.index, y = data['Adj Close'], title = ticker)
        st.plotly_chart(fig)
        #st.plotly_chart(fig, use_container_width=True)
        
    
    # Tabs
        tab1, tab2 = st.tabs(['Fundamental Data', 'Latest News'])
        
        with tab1:
        	st.header("first tab")
        
        with tab2:
            # Boolean to resize the dataframe, stored as a session state variable
            st.checkbox("Use container width", value=False, key="use_container_width")
            
            # Macht die Abfrage in functions.py, ruft StockHero auf
            df = eqs_news(ticker)
            
            # Display the dataframe and allow the user to stretch the dataframe
            # across the full width of the container, based on the checkbox value
            st.dataframe(df, use_container_width=st.session_state.use_container_width, hide_index=True)