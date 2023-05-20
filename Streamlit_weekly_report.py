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

# Display an H2 subheader
st.subheader("S&P500, ETH, BTC price performance over the past 30 days")

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



# Display an H2 subheader
st.subheader("S&P500, ETH, BTC price performance for an arbitrary period in the past and 7-, 30-, 50-, 100- and 200-days moving averages")

min_date = datetime.date(2018, 1, 1)
max_date = current_date
start_date, end_date = st.slider('Select Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))
# Update the chart based on the selected date range

# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
eth = eth[start_date:end_date]
btc = yf.Ticker("BTC-USD").history(period="max")
btc = btc[start_date:end_date]
spy = yf.download('SPY',start_date,end_date)*10

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



# Display an H2 subheader
st.subheader("S&P500, ETH, BTC correlation matrix for an arbitrary period in the past")

# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
eth = eth['2018-01-01':current_date]
btc = yf.Ticker("BTC-USD").history(period="max")
btc = btc['2018-01-01':current_date]

spy = yf.download('SPY','2018-01-01',current_date)*10
eth.index = eth.index.tz_localize(None)
btc.index = btc.index.tz_localize(None)
spy.index = spy.index.tz_localize(None)
eth = eth.drop(eth[~eth.index.isin(spy.index)].index)
btc = btc.drop(btc[~btc.index.isin(spy.index)].index)

spy_lr = (np.log(spy['Close'])-np.log(spy['Close'].shift(1)))[1:].dropna()
btc_lr = (np.log(btc['Close'])-np.log(btc['Close'].shift(1)))[1:].dropna()
eth_lr = (np.log(eth['Close'])-np.log(eth['Close'].shift(1)))[1:].dropna()

min_date = datetime.date(2018, 1, 1)
max_date = current_date
start_date, end_date = st.slider('Select Dates to calculate correlation for', min_value=min_date, max_value=max_date, value=(min_date, max_date))
# Update the chart based on the selected date range

# select the data between start and end dates
spy_lr_1w = spy_lr.loc[start_date:end_date]
btc_lr_1w = btc_lr.loc[start_date:end_date]
eth_lr_1w = eth_lr.loc[start_date:end_date]

# rename columns
spy_lr_1w.columns = ['S&P500']
btc_lr_1w.columns = ['btc']
eth_lr_1w.columns = ['eth']

# calculate correlation coefficients
corr_matrix_1 = pd.concat([spy_lr_1w, btc_lr_1w, eth_lr_1w], axis=1).corr()
corr_matrix_1.index = ['S&P500', 'btc', 'eth']
corr_matrix_1.columns = ['S&P500', 'btc', 'eth']

# Print the correlation matrix
st.write('Correlation matrix for period from', start_date, 'to', end_date)
st.write(corr_matrix_1)




# Display an H2 subheader
st.subheader("S&P500, ETH, BTC correlation for an arbitrary period in the past and 7-, 30-, 50-, 100- and 200-days moving averages")

min_date = datetime.date(2018, 1, 1)
max_date = current_date
start_date, end_date = st.slider('Select Date Range for correlation chart', min_value=min_date, max_value=max_date, value=(min_date, max_date))
# Update the chart based on the selected date range

# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
eth = eth[start_date:end_date]
btc = yf.Ticker("BTC-USD").history(period="max")
btc = btc[start_date:end_date]
spy = yf.download('SPY',start_date,end_date)*10
eth.index = eth.index.tz_localize(None)
btc.index = btc.index.tz_localize(None)
spy.index = spy.index.tz_localize(None)
eth = eth.drop(eth[~eth.index.isin(spy.index)].index)
btc = btc.drop(btc[~btc.index.isin(spy.index)].index)

spy_lr = (np.log(spy['Close'])-np.log(spy['Close'].shift(1)))[1:].dropna()
btc_lr = (np.log(btc['Close'])-np.log(btc['Close'].shift(1)))[1:].dropna()
eth_lr = (np.log(eth['Close'])-np.log(eth['Close'].shift(1)))[1:].dropna()

# Calculate rolling correlation between BTC and SPY
rolling_corr_7_btc_spy = pd.Series(btc_lr).rolling(window=7).corr(spy_lr)
rolling_corr_30_btc_spy = pd.Series(btc_lr).rolling(window=30).corr(spy_lr)
rolling_corr_50_btc_spy = pd.Series(btc_lr).rolling(window=50).corr(spy_lr)
rolling_corr_100_btc_spy = pd.Series(btc_lr).rolling(window=100).corr(spy_lr)
rolling_corr_200_btc_spy = pd.Series(btc_lr).rolling(window=200).corr(spy_lr)

# Calculate rolling correlation between ETH and SPY
rolling_corr_7_eth_spy = pd.Series(eth_lr).rolling(window=7).corr(spy_lr)
rolling_corr_30_eth_spy = pd.Series(eth_lr).rolling(window=30).corr(spy_lr)
rolling_corr_50_eth_spy = pd.Series(eth_lr).rolling(window=50).corr(spy_lr)
rolling_corr_100_eth_spy = pd.Series(eth_lr).rolling(window=100).corr(spy_lr)
rolling_corr_200_eth_spy = pd.Series(eth_lr).rolling(window=200).corr(spy_lr)

# Calculate rolling correlation between BTC and ETH
rolling_corr_7_eth_btc = pd.Series(btc_lr).rolling(window=7).corr(eth_lr)
rolling_corr_30_eth_btc = pd.Series(btc_lr).rolling(window=30).corr(eth_lr)
rolling_corr_50_eth_btc = pd.Series(btc_lr).rolling(window=50).corr(eth_lr)
rolling_corr_100_eth_btc = pd.Series(btc_lr).rolling(window=100).corr(eth_lr)
rolling_corr_200_eth_btc = pd.Series(btc_lr).rolling(window=200).corr(eth_lr)

# Plot data
fig, ax = plt.subplots(figsize=(30,12))
#ax.plot(rolling_corr_7_btc_spy, label="7 day moving average")
ax.plot(rolling_corr_30_btc_spy, label="30 day moving average")
ax.plot(rolling_corr_50_btc_spy, label="50 day moving average")
ax.plot(rolling_corr_100_btc_spy, label="100 day moving average")
ax.plot(rolling_corr_200_btc_spy, label="200 day moving average")

# Add legend and title
ax.legend(fontsize=18)
ax.set_title("BTC and S&P500 Correlation Moving Averages", fontsize=18)
ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Correlation', fontsize=18)

# Plot data
fig2, ax2 = plt.subplots(figsize=(30,12))
#ax2.plot(rolling_corr_7_eth_spy, label="7 day moving average")
ax2.plot(rolling_corr_30_eth_spy, label="30 day moving average")
ax2.plot(rolling_corr_50_eth_spy, label="50 day moving average")
ax2.plot(rolling_corr_100_eth_spy, label="100 day moving average")
ax2.plot(rolling_corr_200_eth_spy, label="200 day moving average")

# Add legend and title
ax2.legend(fontsize=18)
ax2.set_title("ETH and S&P500 Correlation Moving Averages", fontsize=18)
ax2.set_xlabel('Date', fontsize=18)
ax2.set_ylabel('Corellation', fontsize=18)

# Plot data
fig3, ax3 = plt.subplots(figsize=(30,12))
#ax3.plot(rolling_corr_7_eth_btc, label="7 day moving average")
ax3.plot(rolling_corr_30_eth_btc, label="30 day moving average")
ax3.plot(rolling_corr_50_eth_btc, label="50 day moving average")
ax3.plot(rolling_corr_100_eth_btc, label="100 day moving average")
ax3.plot(rolling_corr_200_eth_btc, label="200 day moving average")

# Add legend and title
ax3.legend(fontsize=18)
ax3.set_title("ETH and BTC Correlation Moving Averages", fontsize=18)
ax3.set_xlabel('Date', fontsize=18)
ax3.set_ylabel('Correlation', fontsize=18)

# Display the plot in Streamlit
st.pyplot(fig)

# Display the plot in Streamlit
st.pyplot(fig2)

# Display the plot in Streamlit
st.pyplot(fig3)




# Display an H2 subheader
st.subheader("S&P500, ETH, BTC Annualized volatility for an arbitrary period in the past")

# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
eth = eth['2018-01-01':current_date]
btc = yf.Ticker("BTC-USD").history(period="max")
btc = btc['2018-01-01':current_date]

spy = yf.download('SPY','2018-01-01',current_date)*10
eth.index = eth.index.tz_localize(None)
btc.index = btc.index.tz_localize(None)
spy.index = spy.index.tz_localize(None)
eth = eth.drop(eth[~eth.index.isin(spy.index)].index)
btc = btc.drop(btc[~btc.index.isin(spy.index)].index)

spy_lr = (np.log(spy['Close'])-np.log(spy['Close'].shift(1)))[1:].dropna()
btc_lr = (np.log(btc['Close'])-np.log(btc['Close'].shift(1)))[1:].dropna()
eth_lr = (np.log(eth['Close'])-np.log(eth['Close'].shift(1)))[1:].dropna()

#min_date = datetime.date(2018, 1, 1)
#max_date = current_date
#start_date, end_date = st.slider('Select Dates to calculate Annualized volatility', min_value=min_date, max_value=max_date, value=(min_date, max_date))
# Update the chart based on the selected date range

start_date = st.date_input("Start date for Annualized volatility calculation", value=current_date)
end_date = st.date_input("End date for Annualized volatility calculation", value=current_date)

# select the data between start and end dates
spy_lr_1w = spy_lr.loc[start_date:end_date]
btc_lr_1w = btc_lr.loc[start_date:end_date]
eth_lr_1w = eth_lr.loc[start_date:end_date]

ann_vol_btc_1w = np.std(btc_lr_1w) * np.sqrt(365) * 100
ann_vol_eth_1w = np.std(eth_lr_1w) * np.sqrt(365) * 100
ann_vol_spy_1w = np.std(spy_lr_1w) * np.sqrt(365) * 100

# Print the annualized volatility
st.write('Bitcoin Annualized volatility for period from', start_date, 'to', end_date)
st.write(round(ann_vol_btc_1w,2),' %')

# Print the annualized volatility
st.write('Ethereum Annualized volatility for period from', start_date, 'to', end_date)
st.write(round(ann_vol_eth_1w,2),' %')

# Print the annualized volatility
st.write('S&P500 Annualized volatility for period from', start_date, 'to', end_date)
st.write(round(ann_vol_spy_1w,2),' %')



# Display an H2 subheader
st.subheader("S&P500, ETH, BTC Annualized volatility for an arbitrary period in the past and 7-, 30-, 50-, 100- and 200-days moving averages")

min_date = datetime.date(2018, 1, 1)
max_date = current_date
start_date, end_date = st.slider('Select Date Range for Annualized volatility chart', min_value=min_date, max_value=max_date, value=(min_date, max_date))
# Update the chart based on the selected date range
# Get Ethereum's data from yfinance library
eth = yf.Ticker("ETH-USD").history(period="max")
eth = eth[start_date:end_date]
btc = yf.Ticker("BTC-USD").history(period="max")
btc = btc[start_date:end_date]
spy = yf.download('SPY',start_date,end_date)*10
eth.index = eth.index.tz_localize(None)
btc.index = btc.index.tz_localize(None)
spy.index = spy.index.tz_localize(None)
eth = eth.drop(eth[~eth.index.isin(spy.index)].index)
btc = btc.drop(btc[~btc.index.isin(spy.index)].index)

spy_lr = (np.log(spy['Close'])-np.log(spy['Close'].shift(1)))[1:].dropna()
btc_lr = (np.log(btc['Close'])-np.log(btc['Close'].shift(1)))[1:].dropna()
eth_lr = (np.log(eth['Close'])-np.log(eth['Close'].shift(1)))[1:].dropna()

ann_vol_btc = np.std(btc_lr[-365:])*np.sqrt(365)*100
ann_vol_eth = np.std(eth_lr[-365:])*np.sqrt(365)*100
ann_vol_spy = np.std(spy_lr[-365:])*np.sqrt(365)*100

# Calculate 50, 100, and 200 day moving average
ann_vol_btc_7 = (btc_lr.rolling(window=7).std())*np.sqrt(365)*100
ann_vol_btc_30 = (btc_lr.rolling(window=30).std())*np.sqrt(365)*100
ann_vol_btc_50 = (btc_lr.rolling(window=50).std())*np.sqrt(365)*100
ann_vol_btc_100 = (btc_lr.rolling(window=100).std())*np.sqrt(365)*100
ann_vol_btc_200 = (btc_lr.rolling(window=200).std())*np.sqrt(365)*100

ann_vol_eth_7 = (eth_lr.rolling(window=7).std())*np.sqrt(365)*100
ann_vol_eth_30 = (eth_lr.rolling(window=30).std())*np.sqrt(365)*100
ann_vol_eth_50 = (eth_lr.rolling(window=50).std())*np.sqrt(365)*100
ann_vol_eth_100 = (eth_lr.rolling(window=100).std())*np.sqrt(365)*100
ann_vol_eth_200 = (eth_lr.rolling(window=200).std())*np.sqrt(365)*100

ann_vol_spy_7 = (spy_lr.rolling(window=7).std())*np.sqrt(365)*100
ann_vol_spy_30 = (spy_lr.rolling(window=30).std())*np.sqrt(365)*100
ann_vol_spy_50 = (spy_lr.rolling(window=50).std())*np.sqrt(365)*100
ann_vol_spy_100 = (spy_lr.rolling(window=100).std())*np.sqrt(365)*100
ann_vol_spy_200 = (spy_lr.rolling(window=200).std())*np.sqrt(365)*100

# Plot data
fig, ax = plt.subplots(figsize=(30,12))
ax.plot(ann_vol_btc_7, label="7 day moving average")
ax.plot(ann_vol_btc_30, label="30 day moving average")
ax.plot(ann_vol_btc_50, label="50 day moving average")
ax.plot(ann_vol_btc_100, label="100 day moving average")
ax.plot(ann_vol_btc_200, label="200 day moving average")

# Add legend and title
ax.legend(fontsize=18)
ax.set_title("BTC Annualized Volatility Moving Averages", fontsize=18)
ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel('Annualized Volatility', fontsize=18)

# Plot data
fig2, ax2 = plt.subplots(figsize=(30,12))
ax2.plot(ann_vol_eth_7, label="7 day moving average")
ax2.plot(ann_vol_eth_30, label="30 day moving average")
ax2.plot(ann_vol_eth_50, label="50 day moving average")
ax2.plot(ann_vol_eth_100, label="100 day moving average")
ax2.plot(ann_vol_eth_200, label="200 day moving average")

# Add legend and title
ax2.legend(fontsize=18)
ax2.set_title("ETH Annualized Volatility Moving Averages", fontsize=18)
ax2.set_xlabel('Date', fontsize=18)
ax2.set_ylabel('Annualized Volatility', fontsize=18)

# Plot data
fig3, ax3 = plt.subplots(figsize=(30,12))
ax3.plot(ann_vol_spy_7, label="7 day moving average")
ax3.plot(ann_vol_spy_30, label="30 day moving average")
ax3.plot(ann_vol_spy_50, label="50 day moving average")
ax3.plot(ann_vol_spy_100, label="100 day moving average")
ax3.plot(ann_vol_spy_200, label="200 day moving average")

# Add legend and title
ax3.legend(fontsize=18)
ax3.set_title("S&P500 Annualized Volatility Moving Averages", fontsize=18)
ax3.set_xlabel('Date', fontsize=18)
ax3.set_ylabel('Annualized Volatility', fontsize=18)

# Display the plot in Streamlit
st.pyplot(fig)

# Display the plot in Streamlit
st.pyplot(fig2)

# Display the plot in Streamlit
st.pyplot(fig3)
