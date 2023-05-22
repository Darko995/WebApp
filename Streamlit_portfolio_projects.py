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
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
    except KeyError:  
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_c(data)
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



columns = 3  # Number of columns

with st.form('checkbox_form'):
    st.write('Which project would you like to check?')

    # List of checkbox labels
    checkbox_labels = [
            'volmex', 'filecoin', 'polkadot', 'arbitrum', 'mux',
            'dodo', 'mina', 'liquity', '1inch', 'avalanche',
            'makerdao', 'near-protocol', 'synthetix', 'kyberswap',
            'conflux', '0x', 'immposible-finance', 'centrifuge',
            'uma', 'dhedge', 'cosmos'
        ]

    # Calculate the number of rows
    num_rows = len(checkbox_labels) // columns + 1

    for i in range(num_rows):
        cols_container = st.beta_columns(columns)

        for j in range(columns):
            index = i * columns + j

            if index < len(checkbox_labels):
                cols_container[j].checkbox(label=checkbox_labels[index], key=index)

    submitted = st.form_submit_button('Submit')

    if submitted:
        # Handle form submission logic
        pass

#st.write ('Which project would you like to check?')

#volmex = st.checkbox('volmex')
#filecoin = st.checkbox('filecoin')
#polkadot = st.checkbox('polkadot')
#arbitrum = st.checkbox('arbitrum')
#mcdex = st.checkbox('mux')
#dodo = st.checkbox('dodo')
#mina = st.checkbox('mina')
#liquity = st.checkbox('liquity')
#OneInch = st.checkbox('1inch')
#avalanche = st.checkbox('avalanche')
#makerdao = st.checkbox('makerdao')
#near_protocol = st.checkbox('near-protocol')
#synthetix = st.checkbox('synthetix')
#kyberswap = st.checkbox('kyberswap')
#conflux = st.checkbox('conflux')
#Ox = st.checkbox('0x')
#immposible_finance = st.checkbox('immposible-finance')
#centrifuge = st.checkbox('centrifuge')
#uma = st.checkbox('uma')
#dhedge = st.checkbox('dhedge')
#cosmos = st.checkbox('cosmos')

    if filecoin:
         st.header("Here's some charts for Filecoin!")
         f = portfolio_projects_fdv_timeseries('filecoin')
         # Display the plot in Streamlit
         st.pyplot(f)
    if volmex:
         st.header("Here's some charts for Volmex!")
         #f = portfolio_projects_fdv_timeseries('volmex')
         # Display the plot in Streamlit
         #st.pyplot(f)
    if polkadot:
         st.header("Here's some charts for Polkadot!")
         f = portfolio_projects_fdv_timeseries('polkadot')
         # Display the plot in Streamlit
         st.pyplot(f)
    if arbitrum:
         st.header("Here's some charts for Arbitrum!")
         f = portfolio_projects_fdv_timeseries('arbitrum')
         # Display the plot in Streamlit
         st.pyplot(f)
    if mcdex:
         st.header("Here's some charts for Mcdex!")
         f = portfolio_projects_fdv_timeseries('mux')
         # Display the plot in Streamlit
         st.pyplot(f)
    if dodo:
         st.header("Here's some charts for DODO!")
         f = portfolio_projects_fdv_timeseries('dodo')
         # Display the plot in Streamlit
         st.pyplot(f)
    if mina:
         st.header("Here's some charts for Mina!")
         f = portfolio_projects_fdv_timeseries('mina')
         # Display the plot in Streamlit
         st.pyplot(f)
    if OneInch:
         st.header("Here's some charts for 1inch!")
         f = portfolio_projects_fdv_timeseries('1inch')
         # Display the plot in Streamlit
         st.pyplot(f)
    if avalanche:
         st.header("Here's some charts for Avalanche!")
         f = portfolio_projects_fdv_timeseries('avalanche')
         # Display the plot in Streamlit
         st.pyplot(f)
    if makerdao:
         st.header("Here's some charts for MakerDAO!")
         f = portfolio_projects_fdv_timeseries('makerdao')
         # Display the plot in Streamlit
         st.pyplot(f)
    if near_protocol:
         st.header("Here's some charts for NEAR-protocol!")
         f = portfolio_projects_fdv_timeseries('near-protocol')
         # Display the plot in Streamlit
         st.pyplot(f)
    if synthetix:
         st.header("Here's some charts for Synthetix!")
         f = portfolio_projects_fdv_timeseries('synthetix')
         # Display the plot in Streamlit
         st.pyplot(f)
    if kyberswap:
         st.header("Here's some charts for Kyberswap!")
         f = portfolio_projects_fdv_timeseries('kyberswap')
         # Display the plot in Streamlit
         st.pyplot(f)
    if conflux:
         st.header("Here's some charts for Conflux!")
         f = portfolio_projects_fdv_timeseries('conflux')
         # Display the plot in Streamlit
         st.pyplot(f)
    if Ox:
         st.header("Here's some charts for 0x!")
         f = portfolio_projects_fdv_timeseries('0x')
         # Display the plot in Streamlit
         st.pyplot(f)
    if immposible_finance:
         st.header("Here's some charts for Immposible-finance!")
         f = portfolio_projects_fdv_timeseries('immposible-finance')
         # Display the plot in Streamlit
         st.pyplot(f)
    if centrifuge:
         st.header("Here's some charts for Centrifuge!")
         f = portfolio_projects_fdv_timeseries('centrifuge')
         # Display the plot in Streamlit
         st.pyplot(f)
    if uma:
         st.header("Here's some charts for Uma!")
         f = portfolio_projects_fdv_timeseries('uma')
         # Display the plot in Streamlit
         st.pyplot(f)
    if dhedge:
         st.header("Here's some charts for Dhedge!")
         f = portfolio_projects_fdv_timeseries('dhedge')
         # Display the plot in Streamlit
         st.pyplot(f)
    if cosmos:
         st.header("Here's some charts for Cosmos!")
         f = portfolio_projects_fdv_timeseries('cosmos')
         # Display the plot in Streamlit
         st.pyplot(f)
    if liquity:
         st.header("Here's some charts for Liquity!")
         f = portfolio_projects_fdv_timeseries('liquity')
         # Display the plot in Streamlit
         st.pyplot(f)
