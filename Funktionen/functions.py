# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 13:16:53 2023

@author: rwenzel
"""
import platform

import StockHero as stock
#import yfinance as yf

import streamlit as st
from plotly import graph_objs as go

if platform.system() == "Windows":
    import win32clipboard as clipboard
else:
    import pyperclip as clipboard

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

    #####################
    ###               ###
    ###    EQS News   ###
    ###               ###
    ###               ###
    #####################

@st.cache_data
def eqs_news(isin):
    ticker = stock.Ticker(isin)
    data_load_state = st.text("Load data...")
    t = stock.StockExchange('something')
    data = t.eqs_news_latest_news(10, isin)
    data_load_state.text("Loading data...done!")
    return data

    ##############################
    ###                        ###
    ###    Boersengefluester   ###
    ###                        ###
    ###                        ###
    ##############################
    
@st.cache_data
def boersengefluester(isin):
    ticker = stock.Ticker(isin)
    data_load_state = st.text("Load data...")
    data = ticker.boersengefluester.finanzdaten
    data_load_state.text("Loading data...done!")
    return data

    #####################
    ###               ###
    ###    10 Years   ###
    ###               ###
    ###               ###
    #####################

    # Ermittle alle Unternehmen deren Aktienkurs jedes Jahr höher steht, als im vorherigen Jahr
    # in Bezug auf den Stichtag und ohne Berücksichtigung der Dividenden

@st.cache_data
def ten_year_positive():
    
    # wird verwendet, um Datums- und Zeitoperationen durchzuführen, die über die Standardmethoden von Python hinausgehen
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    # Zeitraum und Fehler 
    # wobei der Fehler nicht wirklich berücksichtigt wird derzeit
    zeitraum, fehler = 10, 0

    # Alle Tickersymbole von der NASDAQ abfragen, die Tickersymbole werden später einzeln abgefragt
    # Das Dataframe enthält auch noch weitere Informationen, wie Name, Industrie, Sector, Market Cap
    data_nasdaq = stock.StockExchange('').nasdaq
    
    # Der Ausgangsdatensatz wird um einiges an Blödsinn bereinigt
    data_nasdaq = data_nasdaq[(data_nasdaq['Market Cap'] != '0.00') & (data_nasdaq['Market Cap'] != '')].reset_index(drop=True)
    
    # Lässt den Bereich freiwählen, sofern gewünscht
    # vielleicht kann man damit später nochmal was machen                                    
    #data = data.iloc[1020: 1080,:].reset_index(drop=True)

    # Aus dem Ausgangs-Dataframe wird eine Series nur mit den Tickersymbolen gemacht
    # braucht man nicht wirklich, lasse ich aber erstmal so
    sdata_ticker = data_nasdaq.iloc[:,0]

    # Ermittelt den Substring der einzelnen Jahre im Abstand von jeweils 1 Jahr der Close/Last Preise
    # über die komplette Länge von 10 Jahren
    def szeitreihe():
        try:
            formated_date = datetime.strptime(data_stock.iloc[0,0], "%m/%d/%Y")
            
            substrings = []
            for i in range(0,10):
                try:
                    reformated_date = formated_date.strftime('%m/%d/%Y')
                    substrings.append(data_stock.loc[data_stock['Date'].str.contains(reformated_date),'Close/Last'].values[0])
                except(IndexError):
                    try:
                        reformated_date = formated_date - relativedelta(days=1)
                        date = reformated_date.strftime('%m/%d/%Y')
                        substrings.append(data_stock.loc[data_stock['Date'].str.contains(date),'Close/Last'].values[0])
                    except(IndexError):
                        try:
                            reformated_date = formated_date - relativedelta(days=2)
                            date = reformated_date.strftime('%m/%d/%Y')
                            substrings.append(data_stock.loc[data_stock['Date'].str.contains(date),'Close/Last'].values[0])
                        except(IndexError):
                            pass
                
                formated_date = formated_date - relativedelta(years=1)
            
            substrings.append(data_stock.iloc[-1,1])
        except(AttributeError):
            substrings = ['$0'] # falls er einen None typ zurückgibt
            
        return substrings

    # Die Funktion entfernt das $ Symbol, das Trennzeichen und wandelt die Werte in einen Float um
    def fzeitreihe():
        substrings_ohne_waehrung = []
        for i in range(0,len(szeitreihe())):
            substrings_ohne_waehrung.append(float(szeitreihe()[i].replace(',', '').replace('$','')))
        
        return substrings_ohne_waehrung

    # Die Funktion zählt die Anzahl, wenn der Wert größer als der vom vorherigen Jahr ist
    def check():
        n = 0
        
        for i in range(0,zeitraum):
            if fzeitreihe()[i] >= fzeitreihe()[i+1]:
                n = n + 1
        return n

    results = []

    ### x Jahre ###
    for symbol in range(0, len(sdata_ticker) - 1):
        data_stock = stock.Ticker(sdata_ticker[symbol]).nasdaq.hist_quotes_stock
        
        # Bei 10 Jahren also 11 Zeichen, wenn weniger Zeichen vorhanden sind dann abbrechen
        if len(szeitreihe()) - 1 >= zeitraum:
            if check() == zeitraum - fehler:
                gesamtperformance = '{:.2%}'.format(fzeitreihe()[0] / fzeitreihe()[-1])
                performance_pa = '{:.2%}'.format(pow(fzeitreihe()[0] / fzeitreihe()[-1], 1 / (len(szeitreihe()) - 1)) - 1)
                
                result = {
                    "Position": symbol,
                    "Ticker": data_nasdaq.iloc[symbol, 0],
                    "Name": data_nasdaq.iloc[symbol, 1],
                    "Industry": data_nasdaq.iloc[symbol, 9],
                    "Sector": data_nasdaq.iloc[symbol, 10],
                    "Market Cap": "{:,}".format(int(data_nasdaq.iloc[symbol, 6].split('.')[0])).replace(",", "."),
                    "10y": gesamtperformance,
                    "p.a.": performance_pa
                }
                st.dataframe(result)
                results.append(result)

    # Ergebnisse in einem Pandas DataFrame anzeigen
    df_results = pd.DataFrame(results)
    
    return df_results