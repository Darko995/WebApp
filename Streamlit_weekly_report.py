import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import requests
import json
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import datetime 

# Get the current date
current_date = datetime.now().date()
# Create a date input widget
start_date = st.date_input("Start date for report", value=current_date)
end_date = st.date_input("End date for report", value=current_date)

st.header('Data Weekly report for period from',start_date,'to',end_date)

# Get the data for the SPY ETF by specifying the stock ticker, start date, and end date
today = datetime.date.today().strftime('%Y-%m-%d')
one_week_ago = (datetime.date.today() - datetime.timedelta(days=35)).strftime('%Y-%m-%d')

# Download the data for the new date range
SPY = yf.download('SPY', one_week_ago, today)*10
SPY_lr = (np.log(SPY)-np.log(SPY.shift(1)))[1:].dropna()

# Get Bitcoin's data from yfinance library
df_btc = yf.Ticker("BTC-USD").history(period="35d")
df_btc = df_btc[['Close']].copy()
df_btc_lr = (np.log(df_btc)-np.log(df_btc.shift(1)))[1:].dropna()

# Get Bitcoin's data from yfinance library
df_eth = yf.Ticker("ETH-USD").history(period="35d")
df_eth = df_eth[['Close']].copy()
df_eth_lr = (np.log(df_eth)-np.log(df_eth.shift(1)))[1:].dropna()

# Remove timezone information from SPY data
SPY.index = SPY.index.tz_localize(None)
df_btc.index = df_btc.index.tz_localize(None)
df_eth.index = df_eth.index.tz_localize(None)

# Drop rows in df that do not have the same index as SPY
#df = df.drop(df[~df.index.isin(SPY.index)].index)
#df_lr = (np.log(df)-np.log(df.shift(1)))[1:].dropna()

# Plot BTC price
fig, ax = plt.subplots(figsize=(28, 14))
ax2 = ax.twinx()

df_btc['Close'].plot(color='crimson', ax=ax2, label='BTC price')

ax2.set_xlabel('Date', fontsize=20)
ax2.set_ylabel('BTC', color='crimson', fontsize=20)

handles2, labels2 = ax2.get_legend_handles_labels()

df_eth['Close'].plot(color='green', ax=ax, label='ETH price')

ax.set_xlabel('Date', fontsize=20)
ax.set_ylabel('ETH', color='green', fontsize=20)

handles, labels = ax.get_legend_handles_labels()

ax.legend(handles, labels, loc='lower left', fontsize=20)
ax2.legend(handles2, labels2, loc='lower right', fontsize=20)

plt.title('Plot BTC and ETH price', fontsize=30)

fig, ax = plt.subplots(figsize=(28, 14))
ax2 = ax.twinx()

SPY['Adj Close'].plot(color='blue', ax=ax, label='S&P 500 price')

ax.set_xlabel('Date', fontsize=20)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='lower left', fontsize=20)

df_btc['Close'].plot(color='crimson', ax=ax2, label='BTC price')

ax2.set_xlabel('Date', fontsize=20)
ax2.set_ylabel('BTC', color='crimson', fontsize=20)

handles2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(handles2, labels2, loc='lower right', fontsize=20)
plt.title('Plot BTC and S&P500 price', fontsize=30)
plt.show()
