# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:02:58 2023

@author: rwenzel
"""

from Funktionen.functions import *

import streamlit as st
import yfinance as yf

from datetime import date, timedelta

class GUI:
    def __init__(self):
        st.set_page_config(page_title="StockHero",layout="wide")
        st.sidebar.title('Options')
        option = st.sidebar.selectbox("Which Dashboard?", ('Market Overview', 'Stock Dashboard', 'Data Resources', 'Experimental'), 0)
        
        if option == 'Market Overview':
            self.cnn_gui()
            
        if option == 'Stock Dashboard':
            self.stock_dashboard_gui()
            
        if option == 'Data Resources':
            self.data_resources_gui()
            
        if option == 'Experimental':
            self.experimental_gui()

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
        st.header('Eingabe')
        
        # Creating two columns:
        left_col, right_col = st.columns([5,4])
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            ticker_symbol = st.text_input('Gib das Ticker-Symbol / ISIN / Namen ein:')
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
        st.header('Eingabe')
        
        # Define custom column widths
        left_col_width, right_col_width, mid_col_width = 6, 4, 3
        
        # Creating three columns:
        left_col, right_col, mid_col = st.columns([left_col_width, right_col_width, mid_col_width])
        
        # Eingabebox für das Ticker-Symbol
        with left_col:
            ticker_symbol = st.text_input('Gib das Ticker-Symbol ein:')
        
        # Zeige das eingegebene Ticker-Symbol an
        with right_col:
            if ticker_symbol:
                st.write(f'Du hast das Ticker-Symbol eingegeben: {ticker_symbol}')
        
        # Button, um den DataFrame zu kopieren
        # Historisches PE-Ratio
        
        try:
            with mid_col:
                if st.button('Historisches PE-Ratio'):
                    df = get_data_gurufocus_pe(ticker_symbol)
                    
                    with left_col:
                        if df is None:
                            st.markdown("")
                            st.warning("Kein PE-Ratio für dieses Symbol vorhanden.")
                            st.markdown("---")  # Trennstrich zwischen den Zeilen
                            st.markdown("Tipp: Sehr wahrscheinlich gibt es kein E im PE-Ratio oder die Eingabe war fehlerhaft.")
                        else:
                            df_markdown = df.to_markdown()
                            set_clipboard_text(df_markdown)
                            st.markdown('DataFrame wurde in die Zwischenablage kopiert.')
                    
                    with right_col:
                        st.write(df)
        
        except Exception as e:
            st.error(f"Fehler beim Kopieren des DataFrames: {e}")        

        
        # Button, um den DataFrame zu kopieren
        # Historisches Debt-to-EBITDA-Ratio
        
        try:
            with mid_col:
                if st.button('Historisches Debt-to-EBITDA-Ratio'):
                    df = get_data_gurufocus_debt_to_ebitda(ticker_symbol)
                    
                    with left_col:
                        if df is None:
                            st.markdown("")
                            st.warning("Kein Debt-to-EBITDA-Ratio für dieses Symbol vorhanden.")
                            st.markdown("---")  # Trennstrich zwischen den Zeilen
                            st.markdown("Tipp: Sehr wahrscheinlich hat das Unternehmen keine Schulden oder die Eingabe war fehlerhaft.")
                        else:
                            df_markdown = df.to_markdown()
                            set_clipboard_text(df_markdown)
                            st.markdown('DataFrame wurde in die Zwischenablage kopiert.')
                        
                    with right_col:
                        st.write(df)
                            
        except Exception as e:
            st.error(f"Fehler beim Kopieren des DataFrames: {e}")        
        
        # Button, um den DataFrame zu kopieren
        # Historische Dividenden-Rendite
        
        try:
            with mid_col:
                if st.button('Historische Dividenden-Rendite'):
                    df = get_data_gurufocus_div_yield(ticker_symbol)
                    
                    with left_col:
                        if df is None:
                            st.warning("Keine Dividendenrenditedaten für dieses Symbol vorhanden.")
                            st.markdown("---")  # Trennstrich zwischen den Zeilen
                            st.markdown("Tipp: Sehr wahrscheinlich schüttet das Unternehmen keine Dividende aus oder die Eingabe war fehlerhaft.")
                        else:    
                            df_markdown = df.to_markdown()
                            set_clipboard_text(df_markdown)
                            st.markdown('DataFrame wurde in die Zwischenablage kopiert.')
                    
                    with right_col:
                        st.write(df)
                        
        except Exception as e:
            st.error(f"Fehler beim Kopieren des DataFrames: {e}")
        
    ################################
    ###                          ###
    ###    Stratosphere GUI      ###
    ###                          ###
    ################################
    
    def stratosphere_gui(self):
        #st.title('Eingabe')
        st.header('Eingabe')
        
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
    
        # Title Main Page
        st.title('Stock Dashboard')
        
        # Sidebar
        st.sidebar.markdown("---")
        isin = st.sidebar.text_input('ISIN', value='DE000STAB1L8')
        
        default_date = date(2024, 1, 1)
        start_date = st.sidebar.date_input('Start Date', value=default_date)
        end_date = st.sidebar.date_input('End Date')
    
        # Main Page
        # Creating two columns:  
        left_col, right_col = st.columns([7, 1])
        
        # Sollte hier mal irgendwas sinnvolleres damit machen
        with right_col:
            
            if st.checkbox('Checkbox'):
                st.balloons()
    
        # Try to download the data
        try:
            data = yf.download(isin, start = start_date, end = end_date)
            
            # Check if the data is empty
            if data.empty:
                st.error("No data found for the given ISIN and date range.")
            else:
                # looking for the Name of the Company in yf data
                isin_data = yf.Ticker(isin)
                longName = isin_data.info['longName']
                
                import plotly.express as px
                
                fig = px.line(data, x = data.index, y = data['Adj Close'], title = longName)
                fig.update_layout(yaxis_title='Adj Close (1d)')
                st.plotly_chart(fig)
                #st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"An error occurred while downloading the data: {e}")
    
        # Tabs
        tab1, tab2, tab3 = st.tabs(['Fundamental Data', 'Latest News', 'Valuation Growth'])
        
        # Boersengefluester
        with tab1:
            st.header("Fundamental Data Overview")
        
            # Get the data
            data_boersengefluester = boersengefluester(isin)
            
            # Pandas DataFrame erstellen
            df = pd.DataFrame(data_boersengefluester)
            
            # Pandas Series erstellen
            #ausgewaehlte_zeilen = df.iloc[[0, 8]]
            
            # Index umbenennen
            #ausgewaehlte_zeilen.index = ['Umsatz'], ['EPS (Diluted)']
            
            # DataFrame in Streamlit anzeigen
            #st.write(ausgewaehlte_zeilen)
            st.write(df)
        
        # EQS-News
        with tab2:
            # Boolean to resize the dataframe, stored as a session state variable
            st.checkbox("Use container width", value=False, key="use_container_width")
            
            # Macht die Abfrage in functions.py, ruft StockHero auf
            df = eqs_news(isin)
            
            # Display the dataframe and allow the user to stretch the dataframe
            # across the full width of the container, based on the checkbox value
            st.dataframe(df, use_container_width=st.session_state.use_container_width, hide_index=True)
        
        # Morningstar
        with tab3:
            df, name_symbol = get_data_morningstar(isin)
            
            #st.subheader('_:blue[Features]_ :sunglasses:')
            
            # Button, um den DataFrame zu kopieren
            if st.button('DataFrame kopieren'):
                if df is not None: 
                    df_markdown = df.to_markdown()
                    set_clipboard_text(df_markdown)
                    st.write('DataFrame wurde in die Zwischenablage kopiert.')
                else:
                    st.write('Keine Daten vorhanden :sunglasses:')
                        
            st.dataframe(df)
            
            
    def data_resources_gui(self):
        # Title Main Page
        #st.title('Data Resources')
        
        # Sidebar
        st.sidebar.markdown("---")
        
        option = st.sidebar.selectbox("Select your target?", ('Stratosphere', 'Morningstar', 'Gurufocus'), 2)
        
        if option == 'Morningstar':
            self.morningstar_gui()

        if option == 'Gurufocus':
            self.gurufocus_gui()
            
        if option == 'Stratosphere':
            self.stratosphere_gui()
        
    def experimental_gui(self):
        
        # Sidebar
        st.sidebar.markdown("---")
        
        option = st.sidebar.selectbox("Select your playground?", ('Forecasting', 'tbd'), 0)
        
        if option == 'Forecasting':
            self.prophet_gui()