import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
import datetime 

st.set_page_config(page_title="Portfolio Priority projects", page_icon="🧐", layout="wide")
# ---- SIDEBAR ----
st.sidebar.header("Please Filter Timeseries Here:")
chart = st.sidebar.multiselect(
    "Select the Metric:",
    options=['FDV', 'MCAP', 'TVL', 'FEES','FEES/TVL','Tokenholders','Active Developers','Code Commits','Trading Volume'],
    default=['FDV', 'MCAP', 'TVL', 'FEES','FEES/TVL','Tokenholders','Active Developers','Code Commits','Trading Volume']
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
        df = df[f'{start_date}':f'{end_date}']
    except KeyError:  
        headers = {"Authorization": st.secrets["APY_KEY"]}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_c(data)
        df = df[f'{start_date}':f'{end_date}']
    except KeyError:
    # Code to handle any other exception
        pass

    df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
    ax.set_title(f"FDV of {project_id} from {start_date} to {end_date}", fontsize=28)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('FDV', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

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
        df = df[f'{start_date}':f'{end_date}']
    except KeyError:
        headers = {"Authorization": st.secrets["APY_KEY"]}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_mcap_c(data)
        df = df[f'{start_date}':f'{end_date}']
      
    df['mcap'].plot(color='crimson', ax=ax, label=f'{project_id} mcap')
    ax.set_title(f"MCAP of {project_id} from {start_date} to {end_date}", fontsize=28)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('MCAP', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

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
        df = df[f'{start_date}':f'{end_date}']
        df['tvl'].plot(color='crimson', ax=ax, label=f'{project_id} tvl')
        ax.set_title(f"TVL of {project_id} from {start_date} to {end_date}", fontsize=28)
        ax.set_xlabel('Date', fontsize=18)
        ax.set_ylabel('TVL', fontsize=18)
        ax.legend(loc='upper left', fontsize=14)
        ax.legend(loc='upper right', fontsize=14)

        return fig
    except KeyError:
        fig, ax = plt.subplots(figsize=(24, 4))

        ax.set_title(f"Sorry, there is no available data for {project_id} TVL!", fontsize=24)
        #ax.set_xlabel('Date', fontsize=18)
        #ax.set_ylabel('TVL', fontsize=18)
        #ax.legend(loc='upper left', fontsize=14)
        #ax.legend(loc='upper right', fontsize=14)

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
        df = df[f'{start_date}':f'{end_date}']
        df['fees'].plot(color='crimson', ax=ax, label=f'{project_id} fees')
        ax.set_title(f"FEES of {project_id} from {start_date} to {end_date}", fontsize=28)
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
        d = d[f'{start_date}':f'{end_date}']
        # Resample the data to weekly frequency
        d_weekly = d.resample('W').last()

        fig, ax = plt.subplots(figsize=(30, 12))
        ax.plot(d_weekly["fees/tvl"], label="fees/tvl")

        # Get the current value of tvl/ss_fees
        #current_value = d_weekly["fees/tvl"].iloc[-1]

        # Add current value as text to the plot
        #ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

        ax.set_title(f"{project_id} Fees and TVL ratio from {start_date} to {end_date}", fontsize=28)
        ax.set_xlabel('Date', fontsize=18)
        ax.set_ylabel('Ratio', fontsize=18)
        return fig     
    except KeyError:
        fig, ax = plt.subplots(figsize=(24, 4))

        ax.set_title(f"Sorry, there is no available data for {project_id} TVL or FEES!", fontsize=24)

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
        
        st.header(f"Here's some charts for {project.capitalize()}!")
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
            st.subheader("Fees/TVL Ratio")
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
        
# ---- HIDE STREAMLIT STYLE ----
#hide_st_style = """
          #  <style>
         #   #MainMenu {visibility: hidden;}
          #  footer {visibility: hidden;}
          #  header {visibility: hidden;}
          #  </style>
          #  """
#st.markdown(hide_st_style, unsafe_allow_html=True)
