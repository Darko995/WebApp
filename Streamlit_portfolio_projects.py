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
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title="Portfolio Priority projects", page_icon="🧐", layout="wide")

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
    st.sidebar.header("Please Filter Timeseries Here:")
    chart = st.sidebar.multiselect(
        "Select the Metric:",
        options=['FDV', 'MCAP', 'TVL', 'FEES','FEES/TVL','Tokenholders','Active Developers','Code Commits','Trading Volume','Price',
                 'Earnings','FDV/FEES','FDV/Tokenholders','FDV/Active Developers','Ann Volatility','MCAP/Trading Volume'],
        default=[]
    )
    # ---- MAINPAGE ----
    st.title(":bar_chart: Portfolio Priority projects")
    st.markdown("##")

    def portfolio_projects_fdv_timeseries(project_id, start_date, end_date):

        def get_data(data):
            date = []
            fdv = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_fully_diluted'])
            dataa = [fdv]
            df = pd.DataFrame(dataa, columns=date, index=['fdv'])
            df = df.T.dropna()
            return df

        def get_data_c(data):
            date = []
            fdv  =[]
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_circulating'])
            dataa = [fdv]
            df = pd.DataFrame(dataa, columns=date, index=['fdv'])
            df = df.T.dropna()
            return df
        try :
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data(data) 
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
            ax.set_title(f"FDV of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('FDV', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            try:
                headers = {"Authorization": st.secrets["APY_KEY"]}

                fig, ax = plt.subplots(figsize=(24, 14))

                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                df = get_data_c(data)
                start_date = pd.Timestamp(start_date).tz_localize(df.index.tz) 
                if start_date > df.index[0]:
                    df = df[f'{start_date}':f'{end_date}']
                df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
                ax.set_title(f"FDV of {project_id}", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('FDV', fontsize=18)
                ax.legend(loc='upper left', fontsize=14)
                ax.legend(loc='upper right', fontsize=14)

                return fig
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} FDV!", fontsize=24)

                return fig

    def portfolio_projects_mcap_timeseries(project_id, start_date, end_date):

        def get_data_mcap(data):
            date = []
            mcap = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                mcap.append(data[i]['market_cap_circulating'])
            dataa = [mcap]
            df = pd.DataFrame(dataa, columns=date, index=['mcap'])
            df = df.T.dropna()
            return df
        def get_data_mcap_c(data):
            date = []
            mcap = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                mcap.append(data[i]['market_cap_fully_diluted'])
            dataa = [mcap]
            df = pd.DataFrame(dataa, columns=date, index=['mcap'])
            df = df.T.dropna()
            return df
        try :
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_mcap(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            df['mcap'].plot(color='crimson', ax=ax, label=f'{project_id} mcap')
            ax.set_title(f"MCAP of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('MCAP', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            try:
                headers = {"Authorization": st.secrets["APY_KEY"]}

                fig, ax = plt.subplots(figsize=(24, 14))

                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                df = get_data_mcap_c(data)
                start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
                if start_date > df.index[0]:
                    df = df[f'{start_date}':f'{end_date}']

                df['mcap'].plot(color='crimson', ax=ax, label=f'{project_id} mcap')
                ax.set_title(f"MCAP of {project_id}", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('MCAP', fontsize=18)
                ax.legend(loc='upper left', fontsize=14)
                ax.legend(loc='upper right', fontsize=14)

                return fig
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} MCAP!", fontsize=24)

                return fig

    def portfolio_projects_tvl_timeseries(project_id, start_date, end_date):

        def get_data_tvl(data):
            date = []
            tvl = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                tvl.append(data[i]['tvl'])
            dataa = [tvl]
            df = pd.DataFrame(dataa, columns=date, index=['tvl'])
            df = df.T.dropna()
            return df
        try:

            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tvl"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_tvl(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            df['tvl'].plot(color='crimson', ax=ax, label=f'{project_id} tvl')
            ax.set_title(f"TVL of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('TVL', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} TVL!", fontsize=24)

            return fig

    def portfolio_projects_fees_timeseries(project_id, start_date, end_date):

        def get_data_fees(data):
            date = []
            fees = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fees.append(data[i]['fees'])
            dataa = [fees]
            df = pd.DataFrame(dataa, columns=date, index=['fees'])
            df = df.T.dropna()
            return df
        try:

            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=fees"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_fees(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            df['fees'].plot(color='crimson', ax=ax, label=f'{project_id} fees')
            ax.set_title(f"FEES of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('FEES', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} FEES!", fontsize=24)
            return fig

    def portfolio_projects_fees_tvl_ratio(project_id, start_date,end_date):
        def get_data_r1(data):
            date = []
            TVL = []
            fees = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                TVL.append(data[i]['tvl'])
                fees.append(data[i]['fees'])
            dataa = [TVL, fees]
            df = pd.DataFrame(dataa, columns=date, index=['TVL', 'fees'])
            df = df.T.dropna()
            return df
        try:
            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tvl%2Cfees"
            headers = {"Authorization": st.secrets["APY_KEY"]}
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            d = get_data_r1(data)
            d = d[::-1]
            d['fees'] = d['fees'].rolling(30).sum().dropna()
            d['fees'] = d['fees'] * (365 / 30)
            d['fees/tvl'] = d['fees']/d['TVL']
            #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
            #if start_date > d.index[0]:
            d = d[f'{start_date}':f'{end_date}']
            # Resample the data to weekly frequency
            d_weekly = d.resample('W').last()

            fig, ax = plt.subplots(figsize=(30, 12))
            ax.plot(d_weekly["fees/tvl"], label="fees/tvl")

            # Get the current value of tvl/ss_fees
            #current_value = d_weekly["fees/tvl"].iloc[-1]

            # Add current value as text to the plot
            #ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

            ax.set_title(f"{project_id} Fees and TVL ratio", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Ratio', fontsize=18)
            return fig     
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} TVL or FEES!", fontsize=24)

            return fig
    def portfolio_projects_volatility_timeseries(project_id, start_date,end_date):

        def get_data_price(data):
            date = []
            price = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                price.append(data[i]['price'])
            dataa = [price]
            df = pd.DataFrame(dataa, columns=date, index=['price'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_price(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            df['price lr'] = (np.log(df['price'])-np.log(df['price'].shift(1)))[1:].dropna()
            #df['vol'] = np.std(df['price lr'][-365:])*np.sqrt(365)*100
            df['vol'] = (df['price lr'].rolling(window=30).std())*np.sqrt(365)*100

            df['vol'].plot(color='crimson', ax=ax, label=f'{project_id} volatility')
            ax.set_title(f"Annualized volatility of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Volatility', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Price!", fontsize=24)

            return fig 
    def portfolio_projects_fdv_fees_ratio(project_id, start_date,end_date):
        def get_data_r2(data):
            date = []
            fdv = []
            fees = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_fully_diluted'])
                fees.append(data[i]['fees'])
            dataa = [fdv, fees]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'fees'])
            df = df.T.dropna()
            return df
        def get_data_r22(data):
            date = []
            fdv = []
            fees = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_circulating'])
                fees.append(data[i]['fees'])
            dataa = [fdv, fees]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'fees'])
            df = df.T.dropna()
            return df
        try:
            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Cfees"
            headers = {"Authorization": st.secrets["APY_KEY"]}
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            d = get_data_r2(data)
            d = d[::-1]
            d['fees'] = d['fees'].rolling(30).sum().dropna()
            d['fees'] = d['fees'] * (365 / 30)
            d['fdv/fees'] = d['fdv']/d['fees']
            #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
            #if start_date > d.index[0]:
            d = d[f'{start_date}':f'{end_date}']
            # Resample the data to weekly frequency
            d_weekly = d.resample('W').last()

            fig, ax = plt.subplots(figsize=(30, 12))
            ax.plot(d_weekly["fdv/fees"], label="fdv/fees")

            # Get the current value of tvl/ss_fees
            #current_value = d_weekly["fees/tvl"].iloc[-1]

            # Add current value as text to the plot
            #ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

            ax.set_title(f"{project_id} FDV and Fees ratio", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Ratio', fontsize=18)
            return fig     
        except KeyError:
            try:
                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating%2Cfees"
                headers = {"Authorization": st.secrets["APY_KEY"]}
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                d = get_data_r22(data)
                d = d[::-1]
                d['fees'] = d['fees'].rolling(30).sum().dropna()
                d['fees'] = d['fees'] * (365 / 30)
                d['fdv/fees'] = d['fdv']/d['fees']
                #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
                #if start_date > d.index[0]:
                d = d[f'{start_date}':f'{end_date}']
                # Resample the data to weekly frequency
                d_weekly = d.resample('W').last()

                fig, ax = plt.subplots(figsize=(30, 12))
                ax.plot(d_weekly["fdv/fees"], label="fdv/fees")

                # Get the current value of tvl/ss_fees
                #current_value = d_weekly["fees/tvl"].iloc[-1]

                # Add current value as text to the plot
                #ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

                ax.set_title(f"{project_id} FDV and Fees ratio", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('Ratio', fontsize=18)
                return fig 
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} Fees!", fontsize=24)

                return fig
    def portfolio_projects_mcap_trading_volume_ratio(project_id, start_date,end_date):
        def get_data_r6(data):
            date = []
            mcap = []
            token_trading_volume = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                mcap.append(data[i]['market_cap_circulating'])
                token_trading_volume.append(data[i]['token_trading_volume'])
            dataa = [mcap, token_trading_volume]
            df = pd.DataFrame(dataa, columns=date, index=['mcap', 'token_trading_volume'])
            df = df.T.dropna()
            return df
        def get_data_r66(data):
            date = []
            mcap = []
            token_trading_volume = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                mcap.append(data[i]['market_cap_fully_diluted'])
                token_trading_volume.append(data[i]['token_trading_volume'])
            dataa = [mcap, token_trading_volume]
            df = pd.DataFrame(dataa, columns=date, index=['mcap', 'token_trading_volume'])
            df = df.T.dropna()
            return df
        try:
            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating%2Ctoken_trading_volume"
            headers = {"Authorization": st.secrets["APY_KEY"]}
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            d = get_data_r6(data)
            d = d[::-1]
            #d['fees'] = d['fees'].rolling(30).sum().dropna()
            #d['fees'] = d['fees'] * (365 / 30)
            d['mcap/token_trading_volume'] = d['mcap']/d['token_trading_volume']
            #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
            #if start_date > d.index[0]:
            d = d[f'{start_date}':f'{end_date}']
            # Resample the data to weekly frequency
            #d_weekly = d.resample('W').last()

            fig, ax = plt.subplots(figsize=(30, 12))
            ax.plot(d["mcap/token_trading_volume"], label="mcap/token_trading_volume")

            ax.set_title(f"{project_id} MCAP and Token Trading Volume ratio", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Ratio', fontsize=18)
            return fig     
        except KeyError:
            try:
                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Cfees"
                headers = {"Authorization": st.secrets["APY_KEY"]}
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                d = get_data_r66(data)
                d = d[::-1]
                #d['fees'] = d['fees'].rolling(30).sum().dropna()
                #d['fees'] = d['fees'] * (365 / 30)
                d['mcap/token_trading_volume'] = d['mcap']/d['token_trading_volume']
                #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
                #if start_date > d.index[0]:
                d = d[f'{start_date}':f'{end_date}']
                # Resample the data to weekly frequency
                #d_weekly = d.resample('W').last()

                fig, ax = plt.subplots(figsize=(30, 12))
                ax.plot(d["mcap/token_trading_volume"], label="mcap/token_trading_volume")

                ax.set_title(f"{project_id} MCAP and Token Trading Volume ratio", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('Ratio', fontsize=18)
                return fig 
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} Token Trading Volume!", fontsize=24)

                return fig
    def portfolio_projects_fdv_tokenholders_ratio(project_id, start_date,end_date):
        def get_data_r3(data):
            date = []
            fdv = []
            tokenholders = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_fully_diluted'])
                tokenholders.append(data[i]['tokenholders'])
            dataa = [fdv, tokenholders]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'tokenholders'])
            df = df.T.dropna()
            return df
        def get_data_r33(data):
            date = []
            fdv = []
            tokenholders = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_circulating'])
                tokenholders.append(data[i]['tokenholders'])
            dataa = [fdv, tokenholders]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'tokenholders'])
            df = df.T.dropna()
            return df
        try:
            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Ctokenholders"
            headers = {"Authorization": st.secrets["APY_KEY"]}
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            d = get_data_r3(data)
            d = d[::-1]
            d['fdv/tokenholders'] = d['fdv']/d['tokenholders']
            #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
            #if start_date > d.index[0]:
            d = d[f'{start_date}':f'{end_date}']
            # Resample the data to weekly frequency
            d_weekly = d.resample('W').last()

            fig, ax = plt.subplots(figsize=(30, 12))
            ax.plot(d_weekly["fdv/tokenholders"], label="fdv/tokenholders")

            ax.set_title(f"{project_id} FDV and Tokenholders Number ratio", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Ratio', fontsize=18)
            return fig     
        except KeyError:
            try:
                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating%2Ctokenholders"
                headers = {"Authorization": st.secrets["APY_KEY"]}
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                d = get_data_r33(data)
                d = d[::-1]
                d['fdv/tokenholders'] = d['fdv']/d['tokenholders']
                #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
                #if start_date > d.index[0]:
                d = d[f'{start_date}':f'{end_date}']
                # Resample the data to weekly frequency
                d_weekly = d.resample('W').last()

                fig, ax = plt.subplots(figsize=(30, 12))
                ax.plot(d_weekly["fdv/tokenholders"], label="fdv/tokenholders")

                ax.set_title(f"{project_id} FDV and Tokenholders Number ratio", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('Ratio', fontsize=18)
                return fig 
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} Tokenholders number!", fontsize=24)

                return fig
    def portfolio_projects_fdv_active_developers_ratio(project_id, start_date,end_date):
        def get_data_r4(data):
            date = []
            fdv = []
            active_developers = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_fully_diluted'])
                active_developers.append(data[i]['active_developers'])
            dataa = [fdv, active_developers]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'active_developers'])
            df = df.T.dropna()
            return df
        def get_data_r44(data):
            date = []
            fdv = []
            active_developers = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                fdv.append(data[i]['market_cap_circulating'])
                active_developers.append(data[i]['active_developers'])
            dataa = [fdv, active_developers]
            df = pd.DataFrame(dataa, columns=date, index=['fdv', 'active_developers'])
            df = df.T.dropna()
            return df
        try:
            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Cactive_developers"
            headers = {"Authorization": st.secrets["APY_KEY"]}
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            d = get_data_r4(data)
            d = d[::-1]
            d['fdv/active_developers'] = d['fdv']/d['active_developers']
            #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
            #if start_date > d.index[0]:
            d = d[f'{start_date}':f'{end_date}']
            # Resample the data to weekly frequency
            #d_weekly = d.resample('W').last()

            fig, ax = plt.subplots(figsize=(30, 12))
            ax.plot(d["fdv/active_developers"], label="fdv/active_developers")

            ax.set_title(f"{project_id} FDV and Active Developers ratio", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Ratio', fontsize=18)
            return fig     
        except KeyError:
            try:
                url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating%2Cactive_developers"
                headers = {"Authorization": st.secrets["APY_KEY"]}
                response = requests.get(url, headers=headers)
                data_shows = json.loads(response.text)
                data = data_shows['data']
                d = get_data_r44(data)
                d = d[::-1]
                d['fdv/active_developers'] = d['fdv']/d['active_developers']
                #start_date = pd.Timestamp(start_date).tz_localize(d.index.tz)
                #if start_date > d.index[0]:
                d = d[f'{start_date}':f'{end_date}']
                # Resample the data to weekly frequency
                #d_weekly = d.resample('W').last()

                fig, ax = plt.subplots(figsize=(30, 12))
                ax.plot(d["fdv/active_developers"], label="fdv/active_developers")

                ax.set_title(f"{project_id} FDV and Active Developers ratio", fontsize=28)
                ax.set_xlabel('Date', fontsize=18)
                ax.set_ylabel('Ratio', fontsize=18)
                return fig 
            except KeyError:
                fig, ax = plt.subplots(figsize=(24, 4))

                ax.set_title(f"Sorry, there is no available data for {project_id} Active Developers!", fontsize=24)

                return fig
    def portfolio_projects_tokenholders_timeseries(project_id, start_date,end_date):

        def get_data_tokenholders(data):
            date = []
            tokenholders = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                tokenholders.append(data[i]['tokenholders'])
            dataa = [tokenholders]
            df = pd.DataFrame(dataa, columns=date, index=['tokenholders'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tokenholders"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_tokenholders(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']

            df['tokenholders'].plot(color='crimson', ax=ax, label=f'{project_id} tokenholders')
            ax.set_title(f"Tokenholders of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Tokenholders number', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Tokenholders number!", fontsize=24)

            return fig


    def portfolio_projects_active_developers_timeseries(project_id, start_date,end_date):

        def get_data_active_developers(data):
            date = []
            active_developers = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                active_developers.append(data[i]['active_developers'])
            dataa = [active_developers]
            df = pd.DataFrame(dataa, columns=date, index=['active_developers'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=active_developers"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_active_developers(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']

            df['active_developers'].plot(color='crimson', ax=ax, label=f'{project_id} active_developers')
            ax.set_title(f"Active developers of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Active developers number', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Active developers number!", fontsize=24)

            return fig
    def portfolio_projects_code_commits_timeseries(project_id, start_date,end_date):

        def get_data_code_commits(data):
            date = []
            code_commits = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                code_commits.append(data[i]['code_commits'])
            dataa = [code_commits]
            df = pd.DataFrame(dataa, columns=date, index=['code_commits'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=code_commits"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_code_commits(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']
            d_weekly = df.resample('W').sum()

            d_weekly['code_commits'].plot(color='crimson', ax=ax, label=f'{project_id} code_commits')
            ax.set_title(f"Code commits of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Weekly Code commits number', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Code commits number!", fontsize=24)

            return fig  

    def portfolio_projects_trading_volume_timeseries(project_id, start_date,end_date):

        def get_data_trading_volume(data):
            date = []
            token_trading_volume = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                token_trading_volume.append(data[i]['token_trading_volume'])
            dataa = [token_trading_volume]
            df = pd.DataFrame(dataa, columns=date, index=['token_trading_volume'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=token_trading_volume"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_trading_volume(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']

            df['token_trading_volume'].plot(color='crimson', ax=ax, label=f'{project_id} token_trading_volume')
            ax.set_title(f"Trading volume of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Trading volume number', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Trading volume!", fontsize=24)

            return fig 
    def portfolio_projects_price_timeseries(project_id, start_date,end_date):

        def get_data_price(data):
            date = []
            price = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                price.append(data[i]['price'])
            dataa = [price]
            df = pd.DataFrame(dataa, columns=date, index=['price'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_price(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']

            df['price'].plot(color='crimson', ax=ax, label=f'{project_id} price')
            ax.set_title(f"Price of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Price', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Price!", fontsize=24)

            return fig 
    def portfolio_projects_earnings_timeseries(project_id, start_date,end_date):

        def get_data_earnings(data):
            date = []
            earnings = []
            for i in range(len(data)):
                date.append(pd.to_datetime((data[i]['timestamp'])))
                earnings.append(data[i]['earnings'])
            dataa = [earnings]
            df = pd.DataFrame(dataa, columns=date, index=['earnings'])
            df = df.T.dropna()
            return df
        try:
            headers = {"Authorization": st.secrets["APY_KEY"]}

            fig, ax = plt.subplots(figsize=(24, 14))

            url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=earnings"
            response = requests.get(url, headers=headers)
            data_shows = json.loads(response.text)
            data = data_shows['data']
            df = get_data_earnings(data)
            start_date = pd.Timestamp(start_date).tz_localize(df.index.tz)
            if start_date > df.index[0]:
                df = df[f'{start_date}':f'{end_date}']

            df['earnings'].plot(color='crimson', ax=ax, label=f'{project_id} earnings')
            ax.set_title(f"Earnings of {project_id}", fontsize=28)
            ax.set_xlabel('Date', fontsize=18)
            ax.set_ylabel('Earnings', fontsize=18)
            ax.legend(loc='upper left', fontsize=14)
            ax.legend(loc='upper right', fontsize=14)

            return fig
        except KeyError:
            fig, ax = plt.subplots(figsize=(24, 4))

            ax.set_title(f"Sorry, there is no available data for {project_id} Earnings!", fontsize=24)

            return fig
    columns = 3  # Number of columns
    selected_projects = []

    with st.form('checkbox_form'):
        st.write('Which project would you like to check?')

        # List of checkbox labels
        checkbox_labels = [
            'dodo','liquity', 'avalanche','arbitrum', 'mux',
            'mina','1inch',
            'makerdao', 'near-protocol', 'synthetix', 'kyberswap',
            'conflux', '0x', 'centrifuge',
            'uma', 'dhedge', 'cosmos','filecoin', 'polkadot'
        ]

        # Calculate the number of rows
        num_rows = len(checkbox_labels) // columns + 1

        for i in range(num_rows):
            cols_container = st.beta_columns(columns)

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
        start_date = st.date_input("Select start date:")
        end_date = st.date_input("Select end date:")
        submitted = st.form_submit_button('Submit')

    if submitted:
        # Display charts for selected projects
        for project in selected_projects:

            st.header(f"Here's charts for {project.capitalize()}!")
            if 'FDV' in chart:
                f = portfolio_projects_fdv_timeseries(project,start_date,end_date)
                st.subheader("Fully diluted valuation")
                st.pyplot(f)
            if 'MCAP' in chart:
                st.subheader("Market capitalization")
                m = portfolio_projects_mcap_timeseries(project,start_date,end_date)
                st.pyplot(m)
            if 'TVL' in chart:
                st.subheader("Total value locked")
                t = portfolio_projects_tvl_timeseries(project,start_date,end_date)
                st.pyplot(t)
            if 'FEES' in chart:
                st.subheader("Fees")
                fees = portfolio_projects_fees_timeseries(project,start_date,end_date)
                st.pyplot(fees)
            if 'FEES/TVL' in chart:
                st.subheader("Annualized Fees/TVL Ratio")
                ftvl = portfolio_projects_fees_tvl_ratio(project,start_date,end_date)
                st.pyplot(ftvl)
            if 'Tokenholders' in chart:
                st.subheader("Tokenholders Number")
                th = portfolio_projects_tokenholders_timeseries(project,start_date,end_date)
                st.pyplot(th)
            if 'Active Developers' in chart:
                st.subheader("Active developers Number")
                th = portfolio_projects_active_developers_timeseries(project,start_date,end_date)
                st.pyplot(th)
            if 'Code Commits' in chart:
                st.subheader("Weekly Code Commits Number")
                cc = portfolio_projects_code_commits_timeseries(project,start_date,end_date)
                st.pyplot(cc)
            if 'Trading Volume' in chart:
                st.subheader("Token Trading Volume")
                tv = portfolio_projects_trading_volume_timeseries(project,start_date,end_date)
                st.pyplot(tv)
            if 'Price' in chart:
                st.subheader("Price")
                pr = portfolio_projects_price_timeseries(project,start_date,end_date)
                st.pyplot(pr)
            if 'Earnings' in chart:
                st.subheader("Earnings")
                ear = portfolio_projects_earnings_timeseries(project,start_date,end_date)
                st.pyplot(ear)
            if 'FDV/FEES' in chart and project!='0x':
                st.subheader("FDV/Annualized FEES Ratio")
                fdvf = portfolio_projects_fdv_fees_ratio(project,start_date,end_date)
                st.pyplot(fdvf)
            if 'FDV/Tokenholders' in chart:
                st.subheader("FDV/Tokenholders Number Ratio")
                fdvth = portfolio_projects_fdv_tokenholders_ratio(project,start_date,end_date)
                st.pyplot(fdvth)
            if 'FDV/Active Developers' in chart:
                st.subheader("FDV/Active Developers Number Ratio")
                fdvcc = portfolio_projects_fdv_active_developers_ratio(project,start_date,end_date)
                st.pyplot(fdvcc)
            if 'Ann Volatility' in chart:
                st.subheader("Annualized Volatility")
                vol = portfolio_projects_volatility_timeseries(project,start_date,end_date)
                st.pyplot(vol)
            if 'MCAP/Trading Volume' in chart:
                st.subheader("MCAP and Token Trading Volume Ratio")
                mcaptv = portfolio_projects_mcap_trading_volume_ratio(project,start_date,end_date)
                st.pyplot(mcaptv)
