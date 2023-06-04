import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import requests
import json
import matplotlib
from matplotlib import pyplot as plt
# Set the maximum number of open figures to 30
matplotlib.rcParams['figure.max_open_warning'] = 30
import numpy as np
import pandas as pd
import yfinance as yf
import datetime 
import matplotlib.dates as mdates
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

st.set_page_config(page_title="Token Vesting Management", page_icon="🧐", layout="wide")
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
# --- USER AUTHENTICATION ---
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')
elif authentication_status:
    authenticator.logout('Logout', 'main', key='unique_key')
    st.write(f'Welcome *{name}*')
    
    # ---- SIDEBAR ----
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    
    
    # ---- MAINPAGE ----
    st.title(":bar_chart: Token Vesting Management")
    st.markdown("##")
    
    def ilv():
        token_ticker = "ILV"
        coingecko_id = "illuvium"
        entry_price = 3
        vesting_schedule = {pd.Timestamp('2022-07-30'):8.33, pd.Timestamp('2022-08-30'):8.33, pd.Timestamp('2022-09-30'):8.33, pd.Timestamp('2022-10-30'):8.33,
                            pd.Timestamp('2022-11-30'):8.33, pd.Timestamp('2022-12-30'):8.33,pd.Timestamp('2023-01-30'):8.33,
                            pd.Timestamp('2023-02-28'):8.33,pd.Timestamp('2023-03-30'):8.34,pd.Timestamp('2023-04-30'):8.34,pd.Timestamp('2023-05-30'):8.34,pd.Timestamp('2023-06-30'):8.34}
        tge_date = "2022-01-01"
        total_tokens_number = 66666.67 

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ilv = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ilv.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ilv.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ilv.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ilv.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ilv.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ilv.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ilv.index = df_ilv.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ilv['next_vesting_date'] = df_ilv['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ilv.index, df_ilv['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')

        return df_ilv,fig

    def ar():
        token_ticker = "AR"
        coingecko_id = "arweave"
        entry_price = 4.63
        vesting_schedule = {pd.Timestamp('2022-02-02'):100}
        tge_date = "2019-11-01"
        total_tokens_number = 250000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ar = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ar.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ar.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ar.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ar.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ar.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ar.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ar.index = df_ar.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ar['next_vesting_date'] = df_ar['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ar.index, df_ar['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        return df_ar,fig

    def snx():
        token_ticker = "SNX"
        coingecko_id = "havven"
        entry_price = 3.1
        vesting_schedule = {pd.Timestamp('2021-12-02'):100}
        tge_date = "2018-03-21"
        total_tokens_number = 241936

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_snx = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_snx.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_snx.loc[date, 'current_roi'] = round(current_roi, 2)
            df_snx.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_snx.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_snx.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_snx.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_snx.index = df_snx.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_snx['next_vesting_date'] = df_snx['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_snx.index, df_snx['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_snx,fig

    
    def ata1():
        token_ticker1 = "ATA"
        coingecko_id1 = "automata"
        entry_price = 0.02
        vesting_schedule = {pd.Timestamp('2021-06-07'):12.5,pd.Timestamp('2021-12-07'):12.5,pd.Timestamp('2022-03-07'):12.5,pd.Timestamp('2022-06-07'):12.5,
                            pd.Timestamp('2022-09-07'):12.5,pd.Timestamp('2022-12-07'):12.5,pd.Timestamp('2023-03-07'):12.5,pd.Timestamp('2023-06-07'):12.5}
        tge_date = "2021-06-07"
        total_tokens_number = 4800000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id1}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id1]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ata1 = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ata1.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ata1.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ata1.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ata1.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ata1.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ata1.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ata1.index = df_ata1.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ata1['next_vesting_date'] = df_ata1['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ata1.index, df_ata1['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_ata1,fig

    def ata2():
        token_ticker2 = "ATA"
        coingecko_id2 = "automata"
        entry_price = 0.04
        vesting_schedule = {pd.Timestamp('2021-06-07'):12.5,pd.Timestamp('2021-12-07'):12.5,pd.Timestamp('2022-03-07'):12.5,pd.Timestamp('2022-06-07'):12.5,pd.Timestamp('2022-09-07'):12.5,
                            pd.Timestamp('2022-12-07'):12.5,pd.Timestamp('2023-03-07'):12.5,pd.Timestamp('2023-06-07'):12.5}
        tge_date = "2021-06-07"
        total_tokens_number = 3750000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id2}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id2]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ata2 = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ata2.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ata2.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ata2.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ata2.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ata2.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ata2.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ata2.index = df_ata2.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ata2['next_vesting_date'] = df_ata2['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ata2.index, df_ata2['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_ata2,fig

    def lqty():
        token_ticker = "LQTY"
        coingecko_id = "liquity"
        entry_price = 0.699
        vesting_schedule = {pd.Timestamp('2022-04-05'):25,pd.Timestamp('2022-05-05'):2.77,pd.Timestamp('2022-06-05'):2.77,pd.Timestamp('2022-07-05'):2.77,pd.Timestamp('2022-08-05'):2.77,
                            pd.Timestamp('2022-09-05'):2.77,pd.Timestamp('2022-10-05'):2.77,pd.Timestamp('2022-11-05'):2.78,pd.Timestamp('2022-12-05'):2.78,pd.Timestamp('2023-01-05'):2.78,
                            pd.Timestamp('2023-02-05'):2.78,pd.Timestamp('2023-03-05'):2.78,pd.Timestamp('2023-04-05'):2.78,pd.Timestamp('2023-05-05'):2.78,pd.Timestamp('2023-06-05'):2.78,
                            pd.Timestamp('2023-07-05'):2.78,pd.Timestamp('2023-08-05'):2.78,pd.Timestamp('2023-09-05'):2.78,pd.Timestamp('2023-10-05'):2.78,pd.Timestamp('2023-11-05'):2.78,
                            pd.Timestamp('2023-12-05'):2.78,pd.Timestamp('2024-01-05'):2.78,pd.Timestamp('2024-02-05'):2.78,pd.Timestamp('2024-03-05'):2.78,pd.Timestamp('2024-04-05'):2.78,
                            pd.Timestamp('2024-05-05'):2.78,pd.Timestamp('2024-06-05'):2.78,pd.Timestamp('2024-07-05'):2.78
                            }
        tge_date = "2021-04-05"
        total_tokens_number = 357143

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_lqty = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_lqty.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_lqty.loc[date, 'current_roi'] = round(current_roi, 2)
            df_lqty.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_lqty.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_lqty.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_lqty.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_lqty.index = df_lqty.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_lqty['next_vesting_date'] = df_lqty['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_lqty.index, df_lqty['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_lqty,fig

    def c98():
        token_ticker = "C98"
        coingecko_id = "coin98"
        entry_price = 0.075
        vesting_schedule = {pd.Timestamp('2022-07-23'):1.92,pd.Timestamp('2022-05-05'):2.77,pd.Timestamp('2022-06-05'):2.77,pd.Timestamp('2022-07-05'):2.77,pd.Timestamp('2022-08-05'):2.77,
                            pd.Timestamp('2022-09-05'):2.77,pd.Timestamp('2022-10-05'):2.77,pd.Timestamp('2022-11-05'):2.77,pd.Timestamp('2022-12-05'):2.77,pd.Timestamp('2023-01-05'):2.77,
                            pd.Timestamp('2023-02-05'):2.77,pd.Timestamp('2023-03-05'):2.77,pd.Timestamp('2023-04-05'):2.77,pd.Timestamp('2023-05-05'):2.77,pd.Timestamp('2023-06-05'):2.77,
                            pd.Timestamp('2023-07-05'):2.77,pd.Timestamp('2023-08-05'):2.77,pd.Timestamp('2023-09-05'):2.77,pd.Timestamp('2023-10-05'):2.77,pd.Timestamp('2023-11-05'):2.77,
                            pd.Timestamp('2023-12-05'):2.77,pd.Timestamp('2024-01-05'):2.77,pd.Timestamp('2024-02-05'):2.77,pd.Timestamp('2024-03-05'):2.77,pd.Timestamp('2024-04-05'):2.77,
                            pd.Timestamp('2024-05-05'):2.77,pd.Timestamp('2024-06-05'):2.77,pd.Timestamp('2024-07-05'):2.77,pd.Timestamp('2024-08-05'):2.77,pd.Timestamp('2024-09-05'):2.77,
                            pd.Timestamp('2024-10-05'):2.77,pd.Timestamp('2024-11-05'):2.77,pd.Timestamp('2024-12-05'):2.77,pd.Timestamp('2025-01-05'):2.77,pd.Timestamp('2025-02-05'):2.77,
                            pd.Timestamp('2025-03-05'):2.77,pd.Timestamp('2023-07-23'):2.77}
        tge_date = "2021-07-23"
        total_tokens_number = 2666667

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_c98 = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_c98.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_c98.loc[date, 'current_roi'] = round(current_roi, 2)
            df_c98.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_c98.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_c98.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_c98.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_c98.index = df_c98.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_c98['next_vesting_date'] = df_c98['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        fig, ax = plt.subplots()
        ax.plot(df_c98.index, df_c98['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        return df_c98,fig

    def uma():
        token_ticker = "UMA"
        coingecko_id = "uma"
        entry_price = 0.963
        vesting_schedule = {pd.Timestamp('2021-08-31'):100}
        tge_date = "2020-04-30"
        total_tokens_number = 6893

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_uma = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_uma.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_uma.loc[date, 'current_roi'] = round(current_roi, 2)
            df_uma.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_uma.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_uma.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_uma.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_uma.index = df_uma.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_uma['next_vesting_date'] = df_uma['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_uma.index, df_uma['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_uma,fig

    def mux():
        token_ticker = "MUX"
        coingecko_id = "mcdex"
        entry_price = 10
        vesting_schedule = {pd.Timestamp('2021-08-31'):100}
        tge_date = "2020-07-13"
        total_tokens_number = 20000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_mcdex = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_mcdex.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_mcdex.loc[date, 'current_roi'] = round(current_roi, 2)
            df_mcdex.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_mcdex.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_mcdex.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_mcdex.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_mcdex.index = df_mcdex.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_mcdex['next_vesting_date'] = df_mcdex['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_mcdex.index, df_mcdex['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_mcdex, fig

    def izi():
        token_ticker = "IZI"
        coingecko_id = "izumi-finance"
        entry_price = 0.02
        vesting_schedule = {pd.Timestamp('2022-12-21'):100}
        tge_date = "2021-12-21"
        total_tokens_number = 16150000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_izumi = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_izumi.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_izumi.loc[date, 'current_roi'] = round(current_roi, 2)
            df_izumi.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_izumi.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_izumi.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_izumi.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_izumi.index = df_izumi.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_izumi['next_vesting_date'] = df_izumi['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_izumi.index, df_izumi['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_izumi, fig

    def insur():
        token_ticker = "INSUR"
        coingecko_id = "insurace"
        entry_price = 0.35
        vesting_schedule = {pd.Timestamp('2023-05-15'):100}
        tge_date = "2021-03-15"
        total_tokens_number = 228571

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_insur = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_insur.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_insur.loc[date, 'current_roi'] = round(current_roi, 2)
            df_insur.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_insur.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_insur.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_insur.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_insur.index = df_insur.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_insur['next_vesting_date'] = df_insur['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_insur.index, df_insur['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_insur, fig

    def thales():
        token_ticker = "THALES"
        coingecko_id = "thales"
        entry_price = 0.33
        vesting_schedule = {pd.Timestamp('2022-09-16'):50,pd.Timestamp('2022-10-16'):4.17,pd.Timestamp('2022-11-16'):4.17,pd.Timestamp('2022-12-16'):4.17,pd.Timestamp('2023-01-16'):4.17,
                            pd.Timestamp('2023-02-16'):4.17,pd.Timestamp('2023-03-16'):4.17,pd.Timestamp('2023-04-16'):4.17,pd.Timestamp('2023-05-16'):4.17,pd.Timestamp('2023-06-16'):4.16,
                            pd.Timestamp('2023-07-16'):4.16,pd.Timestamp('2023-08-16'):4.16,pd.Timestamp('2023-09-16'):4.16}
        tge_date = "2021-09-16"
        total_tokens_number = 303030

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_thales = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_thales.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_thales.loc[date, 'current_roi'] = round(current_roi, 2)
            df_thales.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_thales.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_thales.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_thales.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_thales.index = df_thales.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_thales['next_vesting_date'] = df_thales['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_thales.index, df_thales['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_thales, fig

    def imf():
        token_ticker = "IF"
        coingecko_id = "impossible-finance"
        entry_price = 0.06
        vesting_schedule = {pd.Timestamp('2021-06-18'):25,pd.Timestamp('2022-07-18'):6.25,pd.Timestamp('2022-08-18'):6.25,pd.Timestamp('2022-09-18'):6.25,pd.Timestamp('2022-10-18'):6.25,
                            pd.Timestamp('2022-11-18'):6.25,pd.Timestamp('2022-12-18'):6.25,pd.Timestamp('2023-01-18'):6.25,pd.Timestamp('2023-02-18'):6.25,pd.Timestamp('2023-03-18'):6.25,
                            pd.Timestamp('2023-04-18'):6.25,pd.Timestamp('2023-05-18'):6.25,pd.Timestamp('2023-06-18'):6.25}
        tge_date = "2021-06-18"
        total_tokens_number =   1666666.67 

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_if = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_if.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_if.loc[date, 'current_roi'] = round(current_roi, 2)
            df_if.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_if.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_if.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_if.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_if.index = df_if.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_if['next_vesting_date'] = df_if['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_if.index, df_if['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_if, fig

    def glmr():
        token_ticker = "GLMR"
        coingecko_id = "moonbeam"
        entry_price = 0.05
        vesting_schedule = {pd.Timestamp('2023-01-11'):100}
        tge_date = "2022-02-11"
        total_tokens_number = 5000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_glmr = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_glmr.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_glmr.loc[date, 'current_roi'] = round(current_roi, 2)
            df_glmr.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_glmr.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_glmr.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_glmr.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_glmr.index = df_glmr.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_glmr['next_vesting_date'] = df_glmr['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_glmr.index, df_glmr['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_glmr, fig

    def astr():
        token_ticker = "ASTR"
        coingecko_id = "astar"
        entry_price =   19366666/83000
        vesting_schedule = {pd.Timestamp('2022-07-17'):100}
        tge_date = "2022-01-17"
        total_tokens_number = 19366666

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_astr = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_astr.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_astr.loc[date, 'current_roi'] = round(current_roi, 2)
            df_astr.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_astr.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_astr.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_astr.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_astr.index = df_astr.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_astr['next_vesting_date'] = df_astr['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_astr.index, df_astr['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_astr, fig

    def ujenny():
        token_ticker = "UJENNY"
        coingecko_id = "jenny-metaverse-dao-token"
        entry_price = 1.345 
        vesting_schedule = {pd.Timestamp('2021-05-16'):100}
        tge_date = "2021-05-13"
        total_tokens_number = 148699 

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ujenny = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ujenny.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ujenny.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ujenny.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ujenny.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ujenny.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ujenny.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ujenny.index = df_ujenny.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ujenny['next_vesting_date'] = df_ujenny['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ujenny.index, df_ujenny['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_ujenny, fig

    def fnx():
        token_ticker = "FNX"
        coingecko_id = "FinNexus"
        entry_price = 0.12
        vesting_schedule = {pd.Timestamp('2022-07-03'):100}
        tge_date = "2021-08-13"
        total_tokens_number = 1250000

        # call coingecko api to get real-time price
        #url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        #response = requests.get(url)
        #price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        #current_price = price
        #current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_fnx = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_fnx.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_fnx.loc[date, 'current_roi'] = 'N/A'
            df_fnx.loc[date, 'current_usd_amount'] = 'N/A'
            df_fnx.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_fnx.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_fnx.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_fnx.index = df_fnx.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_fnx['next_vesting_date'] = df_fnx['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_fnx.index, df_fnx['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_fnx, fig

    def swise():
        token_ticker = "SWISE"
        coingecko_id = "stakewise"
        entry_price = 0.12
        vesting_schedule = {pd.Timestamp('2022-06-20'):5.65,pd.Timestamp('2022-07-20'):5.55,pd.Timestamp('2022-08-20'):5.55,pd.Timestamp('2022-09-20'):5.55,
                            pd.Timestamp('2022-10-20'):5.55,pd.Timestamp('2022-11-20'):5.55,pd.Timestamp('2022-12-20'):5.55,pd.Timestamp('2023-01-20'):5.55,
                            pd.Timestamp('2023-02-20'):5.55,pd.Timestamp('2023-03-20'):5.55,pd.Timestamp('2023-04-20'):5.55,pd.Timestamp('2023-05-20'):5.55,
                            pd.Timestamp('2023-06-20'):5.55,pd.Timestamp('2023-07-20'):5.55,pd.Timestamp('2023-08-20'):5.55,pd.Timestamp('2023-09-20'):5.55,
                            pd.Timestamp('2023-10-20'):5.55,pd.Timestamp('2023-11-20'):5.55}
        tge_date = "2021-04-27"
        total_tokens_number = 3333333.33 

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_swise = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_swise.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_swise.loc[date, 'current_roi'] = round(current_roi, 2)
            df_swise.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_swise.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_swise.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_swise.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_swise.index = df_swise.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_swise['next_vesting_date'] = df_swise['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_swise.index, df_swise['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_swise, fig

    def cfg():
        token_ticker = "CFG"
        coingecko_id = "centrifuge"
        entry_price = 0.12
        vesting_schedule = {pd.Timestamp('2021-12-16'):50,pd.Timestamp('2022-01-16'):2.9,pd.Timestamp('2022-01-16'):2.083,pd.Timestamp('2022-02-16'):2.083,
                            pd.Timestamp('2022-03-16'):2.083,pd.Timestamp('2022-04-16'):2.083,pd.Timestamp('2022-05-16'):2.083,pd.Timestamp('2022-06-16'):2.083,
                            pd.Timestamp('2022-07-16'):2.083,pd.Timestamp('2022-08-16'):2.083,pd.Timestamp('2022-09-16'):2.083,pd.Timestamp('2022-10-16'):2.083,
                            pd.Timestamp('2022-11-16'):2.083,pd.Timestamp('2022-12-16'):2.083,pd.Timestamp('2023-01-16'):2.083,pd.Timestamp('2023-02-16'):2.083,
                            pd.Timestamp('2023-03-16'):2.083,pd.Timestamp('2023-04-16'):2.083,pd.Timestamp('2023-05-16'):2.083,pd.Timestamp('2023-06-16'):2.083,
                            pd.Timestamp('2023-07-16'):2.083,pd.Timestamp('2023-08-16'):2.083,pd.Timestamp('2023-09-16'):2.083,pd.Timestamp('2023-10-16'):2.083,
                            pd.Timestamp('2023-11-16'):2.083,pd.Timestamp('2023-12-16'):2.083}
        tge_date = "2021-05-28"
        total_tokens_number = 1666666.67 

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_cfg = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_cfg.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_cfg.loc[date, 'current_roi'] = round(current_roi, 2)
            df_cfg.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_cfg.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_cfg.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_cfg.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_cfg.index = df_cfg.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_cfg['next_vesting_date'] = df_cfg['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_cfg.index, df_cfg['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_cfg, fig

    def gxy():
        token_ticker = "GXY"
        coingecko_id = "galaxy"
        entry_price = 0.075
        vesting_schedule = {pd.Timestamp('2022-02-17'):12,pd.Timestamp('2022-05-17'):11,pd.Timestamp('2022-08-17'):11,pd.Timestamp('2022-11-17'):11,
                            pd.Timestamp('2023-02-17'):11,pd.Timestamp('2023-05-17'):11,pd.Timestamp('2023-08-17'):11,pd.Timestamp('2023-11-17'):11,
                            pd.Timestamp('2024-02-17'):11}
        tge_date = "2022-02-17"
        total_tokens_number = 1333333.33 

        # call coingecko api to get real-time price
        #url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        #response = requests.get(url)
        #price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        #current_price = price
        #current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_gxy = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_gxy.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_gxy.loc[date, 'current_roi'] = 'N/A'
            df_gxy.loc[date, 'current_usd_amount'] = 'N/A'
            df_gxy.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_gxy.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_gxy.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_gxy.index = df_gxy.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_gxy['next_vesting_date'] = df_gxy['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_gxy.index, df_gxy['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_gxy, fig

    def kyve():
        token_ticker = "KYVE"
        coingecko_id = "Kyve network"
        entry_price = 0.1
        vesting_schedule = {pd.Timestamp('2022-12-31'):10,pd.Timestamp('2023-01-31'):5,pd.Timestamp('2023-02-28'):5,pd.Timestamp('2023-03-31'):5,pd.Timestamp('2023-04-30'):5
                            ,pd.Timestamp('2023-05-31'):5,pd.Timestamp('2023-06-30'):5,pd.Timestamp('2023-07-31'):5,pd.Timestamp('2023-08-31'):5,pd.Timestamp('2023-09-30'):5
                            ,pd.Timestamp('2023-10-31'):5,pd.Timestamp('2023-11-30'):5,pd.Timestamp('2023-12-31'):5,pd.Timestamp('2024-01-31'):5,pd.Timestamp('2024-02-28'):5
                            ,pd.Timestamp('2024-03-31'):5,pd.Timestamp('2024-04-30'):5,pd.Timestamp('2024-05-31'):5,pd.Timestamp('2024-06-30'):5}
        tge_date = "2022-12-31"
        total_tokens_number = 1333333.33 

        # call coingecko api to get real-time price
        #url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        #response = requests.get(url)
        #price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        #current_price = price
        #current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_kyve = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_kyve.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_kyve.loc[date, 'current_roi'] = 'N/A'
            df_kyve.loc[date, 'current_usd_amount'] = 'N/A'
            df_kyve.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_kyve.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_kyve.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_kyve.index = df_kyve.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_kyve['next_vesting_date'] = df_kyve['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_kyve.index, df_kyve['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_kyve, fig

    def mina():
        token_ticker = "MINA"
        coingecko_id = "mina-protocol"
        entry_price = 1.86
        vesting_schedule = {pd.Timestamp('2023-02-27'):50,pd.Timestamp('2024-02-27'):2.9}
        tge_date = "2021-06-01"
        total_tokens_number = 537634

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_mina = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_mina.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_mina.loc[date, 'current_roi'] = round(current_roi, 2)
            df_mina.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_mina.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_mina.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_mina.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_mina.index = df_mina.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_mina['next_vesting_date'] = df_mina['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_mina.index, df_mina['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_mina, fig

    def meta():
        token_ticker = "META"
        coingecko_id = "meta-pool"
        entry_price = 0.0006
        vesting_schedule = {}
        start_date = pd.Timestamp('2023-04-26')
        end_date = start_date + pd.DateOffset(days=364)

        for single_date in pd.date_range(start=start_date, end=end_date):
            vesting_schedule[single_date] = 100/365

        tge_date = "2022-03-12"
        total_tokens_number = 1000000000
        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_meta = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_meta.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_meta.loc[date, 'current_roi'] = round(current_roi, 2)
            df_meta.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_meta.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_meta.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_meta.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_meta.index = df_meta.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_meta['next_vesting_date'] = df_meta['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_meta.index, df_meta['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_meta, fig

    def cpr():
        token_ticker = "CPR"
        coingecko_id = "cipher-2"
        entry_price = 0.000926
        vesting_schedule = {pd.Timestamp('2022-09-01'):20,pd.Timestamp('2022-12-01'):10,pd.Timestamp('2023-03-01'):10,
                            pd.Timestamp('2023-06-01'):10,pd.Timestamp('2023-09-01'):10,pd.Timestamp('2023-12-01'):10,
                            pd.Timestamp('2024-03-01'):10,pd.Timestamp('2024-06-01'):10,pd.Timestamp('2024-09-01'):10}
        tge_date = "2022-09-01"
        total_tokens_number = 54000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_cpr = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_cpr.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_cpr.loc[date, 'current_roi'] = round(current_roi, 2)
            df_cpr.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_cpr.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_cpr.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_cpr.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_cpr.index = df_cpr.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_cpr['next_vesting_date'] = df_cpr['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_cpr.index, df_cpr['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_cpr, fig

    def stark():
        #vtoken_ticker = "CPR"
        coingecko_id = "starkware"
        entry_price = 1.93
        vesting_schedule = {pd.Timestamp('2022-11-01'):25,pd.Timestamp('2022-12-01'):2.083,pd.Timestamp('2023-01-01'):2.083,
                            pd.Timestamp('2023-02-01'):2.083,pd.Timestamp('2023-03-01'):2.083,pd.Timestamp('2023-04-01'):2.083,
                            pd.Timestamp('2023-05-01'):2.083,pd.Timestamp('2023-06-01'):2.083,pd.Timestamp('2023-07-01'):2.083,
                            pd.Timestamp('2023-08-01'):2.083,pd.Timestamp('2023-09-01'):2.083,pd.Timestamp('2023-10-01'):2.083,
                            pd.Timestamp('2023-11-01'):2.083,pd.Timestamp('2023-12-01'):2.083,pd.Timestamp('2024-01-01'):2.083,
                            pd.Timestamp('2024-02-01'):2.083,pd.Timestamp('2024-03-01'):2.083,pd.Timestamp('2024-04-01'):2.083,
                            pd.Timestamp('2024-05-01'):2.083,pd.Timestamp('2024-06-01'):2.083,pd.Timestamp('2024-07-01'):2.083,
                            pd.Timestamp('2024-08-01'):2.083,pd.Timestamp('2024-09-01'):2.083,pd.Timestamp('2024-10-01'):2.083,
                            pd.Timestamp('2024-11-01'):2.083,pd.Timestamp('2024-12-01'):2.083,pd.Timestamp('2025-01-01'):2.083,
                            pd.Timestamp('2025-02-01'):2.084,pd.Timestamp('2025-03-01'):2.084,pd.Timestamp('2025-04-01'):2.084,
                            pd.Timestamp('2025-05-01'):2.084,pd.Timestamp('2025-06-01'):2.084,pd.Timestamp('2025-07-01'):2.084,
                            pd.Timestamp('2025-08-01'):2.084,pd.Timestamp('2025-09-01'):2.084,pd.Timestamp('2025-10-01'):2.084,
                            pd.Timestamp('2025-11-01'):2.084}
        tge_date = "2022-01-31"
        total_tokens_number = 96318

        # call coingecko api to get real-time price
        #url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        #response = requests.get(url)
        #price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = 0.036
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_stark = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_stark.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_stark.loc[date, 'current_roi'] = round(current_roi, 2)
            df_stark.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_stark.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_stark.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_stark.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_stark.index = df_stark.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_stark['next_vesting_date'] = df_stark['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_stark.index, df_stark['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_stark, fig

    def aurora():
        token_ticker = "AURORA"
        coingecko_id = "aurora-near"
        entry_price = 0.15
        vesting_schedule = {pd.Timestamp('2022-05-18'):3.25,pd.Timestamp('2022-08-18'):3.25,pd.Timestamp('2022-11-18'):3.5,
                            pd.Timestamp('2023-02-18'):10,pd.Timestamp('2023-05-18'):10,pd.Timestamp('2023-08-18'):10,
                            pd.Timestamp('2023-11-18'):10,pd.Timestamp('2024-02-18'):10,pd.Timestamp('2024-05-18'):10,
                            pd.Timestamp('2024-08-18'):10,pd.Timestamp('2024-11-18'):10,pd.Timestamp('2025-02-18'):10}
        tge_date = "2021-11-18"
        total_tokens_number = 1000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_aurora = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_aurora.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_aurora.loc[date, 'current_roi'] = round(current_roi, 2)
            df_aurora.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_aurora.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_aurora.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_aurora.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_aurora.index = df_aurora.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_aurora['next_vesting_date'] = df_aurora['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_aurora.index, df_aurora['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_aurora, fig

    def rice():
        token_ticker = "RICE"
        coingecko_id = "daosquare"
        entry_price = 0.135
        vesting_schedule = {pd.Timestamp('2022-07-16'):10,pd.Timestamp('2022-10-16'):10,
                            pd.Timestamp('2023-01-16'):10,pd.Timestamp('2023-04-16'):10,pd.Timestamp('2023-07-16'):10,
                            pd.Timestamp('2023-10-16'):10,pd.Timestamp('2024-01-16'):10,pd.Timestamp('2024-04-16'):10,
                            pd.Timestamp('2024-07-16'):10,pd.Timestamp('2024-10-16'):10}
        tge_date = "2021-10-16"
        total_tokens_number = 370370

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_rice = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_rice.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_rice.loc[date, 'current_roi'] = round(current_roi, 2)
            df_rice.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_rice.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_rice.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_rice.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_rice.index = df_rice.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_rice['next_vesting_date'] = df_rice['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_rice.index, df_rice['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_rice, fig

    def brrr():
        token_ticker = "BRRR"
        coingecko_id = "burrow"
        entry_price = 0.05
        vesting_schedule = {pd.Timestamp('2022-12-15'):50,pd.Timestamp('2023-01-15'):50/12,
                            pd.Timestamp('2023-02-15'):50/12,pd.Timestamp('2023-03-15'):50/12,pd.Timestamp('2023-04-15'):50/12,
                            pd.Timestamp('2023-05-15'):50/12,pd.Timestamp('2023-06-15'):50/12,pd.Timestamp('2023-07-15'):50/12,
                            pd.Timestamp('2023-08-15'):50/12,pd.Timestamp('2023-09-15'):50/12,pd.Timestamp('2023-10-15'):50/12,
                            pd.Timestamp('2023-11-15'):50/12,pd.Timestamp('2023-12-15'):50/12}
        tge_date = "2022-06-09"
        total_tokens_number = 2000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_brrr = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_brrr.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_brrr.loc[date, 'current_roi'] = round(current_roi, 2)
            df_brrr.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_brrr.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_brrr.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_brrr.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_brrr.index = df_brrr.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_brrr['next_vesting_date'] = df_brrr['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_brrr.index, df_brrr['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_brrr, fig

    def gtc():
        token_ticker = "GTC"
        coingecko_id = "gitcoin"
        entry_price = 1.6
        vesting_schedule = {pd.Timestamp('2023-11-01'):100/12,pd.Timestamp('2023-12-01'):100/12,pd.Timestamp('2024-01-01'):100/12,
                            pd.Timestamp('2024-02-01'):100/12,pd.Timestamp('2024-03-01'):100/12,pd.Timestamp('2024-04-01'):100/12,
                            pd.Timestamp('2024-05-01'):100/12,pd.Timestamp('2024-06-01'):100/12,pd.Timestamp('2024-07-01'):100/12,
                            pd.Timestamp('2024-08-01'):100/12,pd.Timestamp('2024-09-01'):100/12,pd.Timestamp('2024-10-01'):100/12}
        tge_date = "2021-05-25"
        total_tokens_number = 468750

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=pd.Timestamp('2023-01-01'), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_gtc = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_gtc.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_gtc.loc[date, 'current_roi'] = round(current_roi, 2)
            df_gtc.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_gtc.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_gtc.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_gtc.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_gtc.index = df_gtc.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_gtc['next_vesting_date'] = df_gtc['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_gtc.index, df_gtc['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_gtc, fig

    def magic():
        token_ticker = "MAGIC"
        coingecko_id = "magic"
        entry_price = 0.230072024
        vesting_schedule = {pd.Timestamp('2023-11-18'):100/24,pd.Timestamp('2023-12-18'):100/24,pd.Timestamp('2024-01-18'):100/24,
                            pd.Timestamp('2024-02-18'):100/24,pd.Timestamp('2024-03-18'):100/24,pd.Timestamp('2024-04-18'):100/24,
                            pd.Timestamp('2024-05-18'):100/24,pd.Timestamp('2024-06-18'):100/24,pd.Timestamp('2024-07-18'):100/24,
                            pd.Timestamp('2024-08-18'):100/24,pd.Timestamp('2024-09-18'):100/24,pd.Timestamp('2024-10-18'):100/24,
                            pd.Timestamp('2024-11-18'):100/24,pd.Timestamp('2024-12-18'):100/24,pd.Timestamp('2025-01-18'):100/24,
                            pd.Timestamp('2025-02-18'):100/24,pd.Timestamp('2025-03-18'):100/24,pd.Timestamp('2025-04-18'):100/24,
                            pd.Timestamp('2025-05-18'):100/24,pd.Timestamp('2025-06-18'):100/24,pd.Timestamp('2025-07-18'):100/24,
                            pd.Timestamp('2025-08-18'):100/24,pd.Timestamp('2025-09-18'):100/24,pd.Timestamp('2025-10-18'):100/24,
                            }
        tge_date = "2021-09-27"
        total_tokens_number = 869293

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = price
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=pd.Timestamp('2023-01-01'), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_magic = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_magic.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_magic.loc[date, 'current_roi'] = round(current_roi, 2)
            df_magic.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_magic.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_magic.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_magic.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_magic.index = df_magic.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_magic['next_vesting_date'] = df_magic['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_magic.index, df_magic['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_magic, fig

    def ali():
        token_ticker = "ALI"
        coingecko_id = "alethea-artificial-liquid-intelligence-token"
        entry_price = 0.01
        vesting_schedule = {pd.Timestamp('2023-11-18'):100/24,pd.Timestamp('2023-12-18'):100/24,pd.Timestamp('2024-01-18'):100/24,
                            pd.Timestamp('2024-02-18'):100/24,pd.Timestamp('2024-03-18'):100/24,pd.Timestamp('2024-04-18'):100/24,
                            pd.Timestamp('2024-05-18'):100/24,pd.Timestamp('2024-06-18'):100/24,pd.Timestamp('2024-07-18'):100/24,
                            pd.Timestamp('2024-08-18'):100/24,pd.Timestamp('2024-09-18'):100/24,pd.Timestamp('2024-10-18'):100/24,
                            pd.Timestamp('2024-11-18'):100/24,pd.Timestamp('2024-12-18'):100/24,pd.Timestamp('2025-01-18'):100/24,
                            pd.Timestamp('2025-02-18'):100/24,pd.Timestamp('2025-03-18'):100/24,pd.Timestamp('2025-04-18'):100/24,
                            pd.Timestamp('2025-05-18'):100/24,pd.Timestamp('2025-06-18'):100/24,pd.Timestamp('2025-07-18'):100/24,
                            pd.Timestamp('2025-08-18'):100/24,pd.Timestamp('2025-09-18'):100/24,pd.Timestamp('2025-10-18'):100/24,
                            }
        tge_date = "2022-02-14"
        total_tokens_number = 25000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = 1.05
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=pd.Timestamp('2023-01-01'), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_ali = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_ali.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_ali.loc[date, 'current_roi'] = round(current_roi, 2)
            df_ali.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_ali.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_ali.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_ali.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_ali.index = df_ali.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_ali['next_vesting_date'] = df_ali['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_ali.index, df_ali['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_ali, fig

    def perc():
        token_ticker = "PERC"
        coingecko_id = "perion"
        entry_price = 0.6
        vesting_schedule = {pd.Timestamp('2022-02-06'):10,pd.Timestamp('2023-02-03'):90/12,pd.Timestamp('2023-03-03'):90/12,
                            pd.Timestamp('2023-04-03'):90/12,pd.Timestamp('2023-05-03'):90/12,pd.Timestamp('2023-06-03'):90/12,
                            pd.Timestamp('2023-07-03'):90/12,pd.Timestamp('2023-08-03'):90/12,pd.Timestamp('2023-09-03'):90/12,
                            pd.Timestamp('2023-10-03'):90/12,pd.Timestamp('2023-11-03'):90/12,pd.Timestamp('2023-12-03'):90/12,
                            pd.Timestamp('2024-01-03'):90/12,pd.Timestamp('2024-02-03'):100/12,
                            }
        tge_date = "2022-02-03"
        total_tokens_number = 1000000

        # call coingecko api to get real-time price
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coingecko_id}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[coingecko_id]["usd"]

        # calculate current ROI
        current_price = 1.05
        current_roi = (current_price - entry_price) / entry_price * 100

        # Create a list of dates from the first date in the vesting schedule until today
        dates = pd.date_range(start=min(vesting_schedule.keys()), end=pd.Timestamp.today(), freq='D')

        # Create an empty dataframe
        df_perc = pd.DataFrame(index=dates, columns=['current_token_amount', 'current_roi', 'current_usd_amount', 'next_vesting_date'])

        # Calculate the cumulative sum of unlocked tokens
        unlocked_tokens = 0
        unlocked_pct_tokens = 0
        # Fill in the dataframe with the calculated values
        for date in dates:
            unlocked_pct_tokens += vesting_schedule.get(date, 0)  # Add the percentage for the current date
            unlocked_tokens += (total_tokens_number * vesting_schedule.get(date, 0) / 100)
            df_perc.loc[date, 'current_token_amount'] = round(unlocked_tokens, 2)
            df_perc.loc[date, 'current_roi'] = round(current_roi, 2)
            df_perc.loc[date, 'current_usd_amount'] = round(unlocked_tokens * current_price,2)
            df_perc.loc[date, 'next_vesting_date'] = min([v for v in vesting_schedule.keys() if v > date], default='N/A')
            df_perc.loc[date, 'end_of_vesting'] = list(vesting_schedule.keys())[-1]
            df_perc.loc[date, 'unlocked_pct_tokens'] = round(unlocked_pct_tokens,2)  # Add the sum of percentages

        # Change the index to only display the date part
        df_perc.index = df_perc.index.date
        # Change the dates in the next_vesting_date column to only display the date part
        df_perc['next_vesting_date'] = df_perc['next_vesting_date'].apply(lambda x: x.date() if x != 'N/A' else 'N/A')
        
        fig, ax = plt.subplots()
        ax.plot(df_perc.index, df_perc['unlocked_pct_tokens'])
        # Set the x-axis formatter to display dates in a readable format
        ax.xaxis.set_major_locator(mdates.MonthLocator())  # Display major ticks on a monthly basis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # Format dates as 'YYYY-MM-DD'

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)
        # Set the labels and title of the chart
        ax.set_xlabel('Date')
        ax.set_ylabel('Unlocked %')
        ax.set_title('Unlocked Tokens %')
        
        return df_perc, fig
    
    columns = 3  # Number of columns
    selected_projects = []

    with st.form('checkbox_form'):
        st.write('Which project would you like to check?')

        # List of checkbox labels
        checkbox_labels = [
            'Illuvium','Arweave', 'Synthetix','Automata', 'Liquity',
            'Coin98','Uma', 'Mcdex', 'Izumi', 'Insurace', 'Thales',
            'Impossible finance', 'Moonbeam', 'Astar', 'uJenny',
            'Finnexus', 'Stakewise', 'Centrifuge',
            'Galaxy', 'Kyve network', 'Mina','Meta pool', 'Cypher MOD',
            'Starkware', 'Aurora', 'Daosquare', 'Burrow', 'Gitcoin', 'Treasure DAO', 'Alethea', 'Perion'
        ]

        # Calculate the number of rows
        num_rows = len(checkbox_labels) // columns + 1

        for i in range(num_rows):
            cols_container = st.columns(columns)

            for j in range(columns):
                index = i * columns + j

                if index < len(checkbox_labels):
                    # Store the checkbox value in a variable
                    checkbox_value = cols_container[j].checkbox(
                        label=checkbox_labels[index], key=index
                    )

                    # Add the selected project to the list
                    if checkbox_value:
                        selected_projects.append(checkbox_labels[index])
        submitted = st.form_submit_button('Submit')

    #if submitted:
        # Display charts for selected projects
        for project in selected_projects:

            st.header(f"Here's Token Vesting Schedule for {project.capitalize()}!")
            if project=='Illuvium':
                st.subheader("Illuvium token vesting schedule")
                df_ilv, f = ilv()
                current_token_amount = df_ilv['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = df_ilv['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = df_ilv['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = df_ilv['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = df_ilv['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = df_ilv['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Arweave':
                st.subheader("Arweave token vesting schedule")
                df_ar,f = ar()
                current_token_amount = df_ar['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = df_ar['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = df_ar['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = df_ar['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = df_ar['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = df_ar['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Synthetix':
                st.subheader("Synthetix token vesting schedule")
                d,f = snx()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Automata':
                st.subheader("Automata token vesting schedule")
                d1,f1 = ata1()
                d2,f2 = ata2()
                current_token_amount = d1['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount of Automata 1:** {current_token_amount}")
                current_roi = d1['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI of Automata 1:** {current_roi}")
                current_usd_amount = d1['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount of Automata 1:** {current_usd_amount}")
                next_vesting_date = d1['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date for Automata 1:** {next_vesting_date}")
                end_of_vesting = d1['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting for Automata 1:** {end_of_vesting}")
                unlocked_pct_tokens = d1['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens of Automata 1:** {unlocked_pct_tokens}")
                st.pyplot(f1)
                
                current_token_amount = d2['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount of Automata 2:** {current_token_amount}")
                current_roi = d2['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI of Automata 2:** {current_roi}")
                current_usd_amount = d2['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount of Automata 2:** {current_usd_amount}")
                next_vesting_date = d2['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date for Automata 2:** {next_vesting_date}")
                end_of_vesting = d2['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting for Automata 2:** {end_of_vesting}")
                unlocked_pct_tokens = d2['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens of Automata 2:** {unlocked_pct_tokens}")
                st.pyplot(f2)
            if project=='Liquity':
                st.subheader("Liquity token vesting schedule")
                d,f = lqty()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Coin98':
                st.subheader("Coin98 token vesting schedule")
                d,f = c98()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Uma':
                st.subheader("Uma token vesting schedule")
                d,f = uma()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Mcdex':
                st.subheader("Mcdex token vesting schedule")
                d,f = mux()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Insurace':
                st.subheader("Izumi token vesting schedule")
                d,f = insur()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Izumi':
                st.subheader("Izumi token vesting schedule")
                d,f = izi()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Thales':
                st.subheader("Thales token vesting schedule")
                d,f = thales()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Impossible finance':
                st.subheader("Impossible finance token vesting schedule")
                d,f = imf()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Moonbeam':
                st.subheader("Moonbeam token vesting schedule")
                d,f = glmr()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Astar':
                st.subheader("Astar token vesting schedule")
                d,f = astr()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='uJenny':
                st.subheader("uJenny token vesting schedule")
                d,f = ujenny()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Finnexus':
                st.subheader("Finnexus token vesting schedule")
                d,f = fnx()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Stakewise':
                st.subheader("Stakewise token vesting schedule")
                d,f = swise()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Centrifuge':
                st.subheader("Centrifuge token vesting schedule")
                d,f = cfg()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Galaxy':
                st.subheader("Galaxy token vesting schedule")
                d,f = gxy()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Kyve network':
                st.subheader("Kyve network token vesting schedule")
                d,f = kyve()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Mina':
                st.subheader("Mina token vesting schedule")
                d,f = mina()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Meta pool':
                st.subheader("Meta pool token vesting schedule")
                d,f = meta()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Cypher MOD':
                st.subheader("Cypher MOD token vesting schedule")
                d,f = cpr()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Starkware':
                st.subheader("Starkware token vesting schedule")
                d,f = stark()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Aurora':
                st.subheader("Aurora token vesting schedule")
                d,f = aurora()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Daosquare':
                st.subheader("Daosquare token vesting schedule")
                d,f = rice()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Burrow':
                st.subheader("Burrow token vesting schedule")
                d,f = brrr()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Gitcoin':
                st.subheader("Gitcoin token vesting schedule")
                d,f = gtc()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Treasure DAO':
                st.subheader("Treasure DAO token vesting schedule")
                d,f = magic()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Alethea':
                st.subheader("Alethea MOD token vesting schedule")
                d,f = ali()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
            if project=='Perion':
                st.subheader("Perion MOD token vesting schedule")
                d,f = perc()
                current_token_amount = d['current_token_amount'].iloc[-1]
                st.markdown(f"**Current Token Amount:** {current_token_amount}")
                current_roi = d['current_roi'].iloc[-1]
                st.markdown(f"**Current ROI:** {current_roi}")
                current_usd_amount = d['current_usd_amount'].iloc[-1]
                st.markdown(f"**Current USD amount:** {current_usd_amount}")
                next_vesting_date = d['next_vesting_date'].iloc[-1]
                st.markdown(f"**Next vesting date:** {next_vesting_date}")
                end_of_vesting = d['end_of_vesting'].iloc[-1]
                st.markdown(f"**End of vesting:** {end_of_vesting}")
                unlocked_pct_tokens = d['unlocked_pct_tokens'].iloc[-1]
                st.markdown(f"**Unlocked % of Tokens:** {unlocked_pct_tokens}")
                st.pyplot(f)
