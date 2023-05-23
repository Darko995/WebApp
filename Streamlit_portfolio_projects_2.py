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
        fdv = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            fdv.append(data[i]['market_cap_circulating'])
        dataa = [fdv]
        df = pd.DataFrame(dataa, columns=date, index=['fdv'])
        df = df.T.dropna()
        return df

    try:
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

    # Filter the data based on start and end dates
    df = df.loc[start_date:end_date]

    df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
    ax.set_title(f"FDV of {project_id}", fontsize=18)
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

    try:
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_mcap(data)
    except KeyError:
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_mcap_c(data)

    # Filter the data based on start and end dates
    df = df.loc[start_date:end_date]

    df['mcap'].plot(color='crimson', ax=ax, label=f'{project_id} mcap')
    ax.set_title(f"MCAP of {project_id}", fontsize=18)
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

        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tvl"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_tvl(data)

        # Filter the data based on start and end dates
        df = df.loc[start_date:end_date]

        df['tvl'].plot(color='crimson', ax=ax, label=f'{project_id} tvl')
        ax.set_title(f"TVL of {project_id}", fontsize=18)
        ax.set_xlabel('Date', fontsize=18)
        ax.set_ylabel('TVL', fontsize=18)
        ax.legend(loc='upper left', fontsize=14)
        ax.legend(loc='upper right', fontsize=14)

        return fig
    except KeyError:
        fig, ax = plt.subplots(figsize=(24, 4))

        ax.set_title(f"Sorry, there is no available data for {project_id} TVL!", fontsize=24)
        # ax.set_xlabel('Date', fontsize=18)
        # ax.set_ylabel('TVL', fontsize=18)
        # ax.legend(loc='upper left', fontsize=14)
        # ax.legend(loc='upper right', fontsize=14)

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

        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

        fig, ax = plt.subplots(figsize=(24, 14))

        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=fees"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data_fees(data)

        # Filter the data based on start and end dates
        df = df.loc[start_date:end_date]

        df['fees'].plot(color='crimson', ax=ax, label=f'{project_id} fees')
        ax.set_title(f"FEES of {project_id}", fontsize=18)
        ax.set_xlabel('Date', fontsize=18)
        ax.set_ylabel('FEES', fontsize=18)
        ax.legend(loc='upper left', fontsize=14)
        ax.legend(loc='upper right', fontsize=14)

        return fig
    except KeyError:
        fig, ax = plt.subplots(figsize=(24, 4))

        ax.set_title(f"Sorry, there is no available data for {project_id} FEES!", fontsize=24)
        # ax.set_xlabel('Date', fontsize=18)
        # ax.set_ylabel('TVL', fontsize=18)
        # ax.legend(loc='upper left', fontsize=14)
        # ax.legend(loc='upper right', fontsize=14)

        return fig


columns = 3  # Number of columns
selected_projects = []

with st.form('checkbox_form'):
    st.write('Which project would you like to check?')

    # List of checkbox labels
    checkbox_labels = [
        'filecoin', 'polkadot', 'arbitrum', 'mux',
        'dodo', 'mina', 'liquity', '1inch', 'avalanche',
        'makerdao', 'near-protocol', 'synthetix', 'kyberswap',
        'conflux', '0x', 'centrifuge',
        'uma', 'dhedge', 'cosmos'
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

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if start_date > end_date:
        st.error("Error: The start date should be before the end date.")
    else:
        st.write("Selected projects:", selected_projects)

        for project in selected_projects:
            st.subheader(f"Timeseries analysis for {project}")

            # Plot the FDV timeseries
            fig_fdv = portfolio_projects_fdv_timeseries(project, start_date, end_date)
            st.pyplot(fig_fdv)

            # Plot the MCAP timeseries
            fig_mcap = portfolio_projects_mcap_timeseries(project, start_date, end_date)
            st.pyplot(fig_mcap)

            # Plot the TVL timeseries
            fig_tvl = portfolio_projects_tvl_timeseries(project, start_date, end_date)
            st.pyplot(fig_tvl)

            # Plot the Fees timeseries
            fig_fees = portfolio_projects_fees_timeseries(project, start_date, end_date)
            st.pyplot(fig_fees)
