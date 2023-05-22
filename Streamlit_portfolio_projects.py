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

def portfolio_projects_fdv_timeseries(project_id):

    """
      This Python function named "portfolio_projects_fdv_timeseries" takes in two arguments: a list of project IDs and a start date.
      The function retrieves fdv data for each project ID and generates a line plot of the fdv over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_fdv import multi_project_fdv
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_fdv(project_ids, start_date)
        
      """
      
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
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    df = get_data(data)
        
    df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
    ax.set_title(f"FDV of {project_id}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('FDV', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

# Get the current date
#current_date = datetime.now().date()
# Create a date input widget
#start_date = st.date_input("Start date for report", value=current_date)
#end_date = st.date_input("End date for report", value=current_date)

st.write ('Which project would you like to check?')

volmex = st.checkbox('volmex')
filecoin = st.checkbox('filecoin')
polkadot = st.checkbox('polkadot')
arbitrum = st.checkbox('arbitrum')
mux = st.checkbox('mux')
dodo = st.checkbox('dodo')
mina = st.checkbox('mina')
liquity = st.checkbox('liquity')

if volmex:
     st.header("Great! Here's some charts for volmex")
     portfolio_projects_fdv_timeseries('volmex')
     
