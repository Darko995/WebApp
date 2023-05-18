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
current_date = datetime.datetime.now().date()
# Create a date input widget
start_date = st.date_input("Start date for report", value=current_date)
end_date = st.date_input("End date for report", value=current_date)

# Format the header text
header_text = f"Data Weekly report for period from {start_date} to {end_date}"

# Display the header
st.header(header_text)

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

# Display the plot in Streamlit
st.pyplot(fig)

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

# Display the plot in Streamlit
st.pyplot(fig)




# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
btc = yf.Ticker("BTC-USD").history(period="max")
spy = yf.download('SPY','2015-01-14', current_date)*10

# Calculate 50, 100, and 200 day moving average
eth["7_day_MA"] = eth["Close"].rolling(window=7).mean()
eth["30_day_MA"] = eth["Close"].rolling(window=30).mean()
eth["50_day_MA"] = eth["Close"].rolling(window=50).mean()
eth["100_day_MA"] = eth["Close"].rolling(window=100).mean()
eth["200_day_MA"] = eth["Close"].rolling(window=200).mean()

btc["7_day_MA"] = btc["Close"].rolling(window=7).mean()
btc["30_day_MA"] = btc["Close"].rolling(window=30).mean()
btc["50_day_MA"] = btc["Close"].rolling(window=50).mean()
btc["100_day_MA"] = btc["Close"].rolling(window=100).mean()
btc["200_day_MA"] = btc["Close"].rolling(window=200).mean()

spy["7_day_MA"] = spy["Close"].rolling(window=7).mean()
spy["30_day_MA"] = spy["Close"].rolling(window=30).mean()
spy["50_day_MA"] = spy["Close"].rolling(window=50).mean()
spy["100_day_MA"] = spy["Close"].rolling(window=100).mean()
spy["200_day_MA"] = spy["Close"].rolling(window=200).mean()

# Plot data
fig, ax = plt.subplots(figsize=(30,12))
ax.plot(eth["Close"], label="Price")
ax.plot(eth["7_day_MA"], label="7 day moving average")
ax.plot(eth["30_day_MA"], label="30 day moving average")
ax.plot(eth["50_day_MA"], label="50 day moving average")
ax.plot(eth["100_day_MA"], label="100 day moving average")
ax.plot(eth["200_day_MA"], label="200 day moving average")

# Add legend and title
ax.legend(fontsize=18)
ax.set_title("Ethereum Price and Moving Averages", fontsize=18)
ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Price', fontsize=18)

# Plot data
fig2, ax2 = plt.subplots(figsize=(30,12))
ax2.plot(btc["Close"], label="Price")
ax2.plot(btc["7_day_MA"], label="7 day moving average")
ax2.plot(btc["30_day_MA"], label="30 day moving average")
ax2.plot(btc["50_day_MA"], label="50 day moving average")
ax2.plot(btc["100_day_MA"], label="100 day moving average")
ax2.plot(btc["200_day_MA"], label="200 day moving average")

# Add legend and title
ax2.legend(fontsize=18)
ax2.set_title("Bitcoin Price and Moving Averages", fontsize=18)
ax2.set_xlabel('Date', fontsize=18)
ax2.set_ylabel('Price', fontsize=18)

# Plot data
fig3, ax3 = plt.subplots(figsize=(30,12))
ax3.plot(spy["Close"], label="Price")
ax3.plot(spy["7_day_MA"], label="7 day moving average")
ax3.plot(spy["30_day_MA"], label="30 day moving average")
ax3.plot(spy["50_day_MA"], label="50 day moving average")
ax3.plot(spy["100_day_MA"], label="100 day moving average")
ax3.plot(spy["200_day_MA"], label="200 day moving average")

# Add legend and title
ax3.legend(fontsize=18)
ax3.set_title("S&P500 Price and Moving Averages", fontsize=18)
ax3.set_xlabel('Date', fontsize=18)
ax3.set_ylabel('Price', fontsize=18)

# Display the plot in Streamlit
st.pyplot(fig)

# Display the plot in Streamlit
st.pyplot(fig2)

# Display the plot in Streamlit
st.pyplot(fig3)
