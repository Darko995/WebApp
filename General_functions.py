import TokenTerminal_Functions_2 as tt
import CoinGeckoFunctions_2 as cgf
import FundamentalFunctions as ff
import DefiLlamaFunctions as dl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import matplotlib.dates as mdates
import datetime as dt
import seaborn as sns
from tokenterminal import TokenTerminal
token_terminal = TokenTerminal(key='6c37f0ff-5c2b-4564-8286-3bccf6e42fd2')
cg = CoinGeckoAPI()

def multi_project_df(project_ids):
    """
    This function retrieves metrics data for multiple cryptocurrency projects from an API and
    creates a dataframe with various financial metrics for each project.
    It takes a list of project_ids as input and returns a pandas dataframe with financial metrics such as:
    daily average volume, annualized volume, annualized fees, annualized revenue,
    TVL (Total Value Locked), TVL turnover, token price, realized volatility, market cap (MC),
    fully diluted valuation (FDV), MC/AF, FDV/AF, MC/AR, FDV/AR, MC/TVL, and FDV/TVL.

    To use this function, import it into your python script and call it with a list of project_ids as an argument.
    The resulting dataframe can be used for financial analysis and comparisons between different projects.

    Example usage:

    from multi_project_df import multi_project_df
    project_ids = ['bitcoin', 'ethereum']
    result = multi_project_df(project_ids)

    """
    def get_data(data):
        date = []
        price = []
        FDV  =[]
        volume = []
        fees  = []
        revenue  = []
        TVL = []
        MCAP  = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            price.append(data[i]['price'])
            FDV.append(data[i]['market_cap_fully_diluted'])
            volume.append(data[i]['trading_volume'])
            fees.append(data[i]['fees'])
            revenue.append(data[i]['revenue'])
            TVL.append(data[i]['tvl'])
            MCAP.append(data[i]['market_cap_circulating'])
        dataa = [price,FDV,volume,fees,revenue,TVL,MCAP]
        df = pd.DataFrame(dataa, columns=date, index=['Price','FDV','Volume','Fees','Revenue','TVL','MCAP'])
        df = df.T.dropna()
        return df

    df_list = []
    for project_id in project_ids:
        url1 = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price%2Cmarket_cap_fully_diluted%2Ctvl%2Ctrading_volume%2Cfees%2Crevenue%2Cmarket_cap_circulating"
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
        response1 = requests.get(url1, headers=headers)
        data_shows1 = json.loads(response1.text)
        data1 = data_shows1['data']
        d1 = get_data(data1)  
        d1 = d1[::-1]

        d1['RETURN'] = (d1['Price']/d1['Price'].shift(1)) - 1

        volume, tvl, price, fee, revenue, mcap, mcapfd = d1['Volume'],d1['TVL'], d1['Price'], d1['Fees'], d1['Revenue'], d1['FDV'], d1['MCAP']

        daily_avg_volume = volume[-30:].mean()
        annualized_volume = daily_avg_volume * 365

        daily_avg_fees = fee[-30:].mean()
        annualized_fees = daily_avg_fees * 365

        daily_avg_revenue = revenue[-30:].mean()
        annualized_revenue = daily_avg_revenue * 365

        tvl_current = tvl[-1]
        tvl_turnover = volume[-30:].sum() / tvl[-30:].mean()
        token_price = price[-1]
        realized_volatility = np.std(price[-30:]) * np.sqrt(365) * 100
        mc = mcap[-1]
        fdv = mcapfd[-1]
        mc_af = mc/annualized_fees
        fdv_af = fdv/annualized_fees
        mc_ar = mc/annualized_revenue
        fdv_ar = fdv/annualized_revenue
        mc_tvl = mc/tvl_current
        fdv_tvl = fdv/tvl_current

        titles = ['Daily Average Volume', 'Annualized Volume', 'Annualized Fees (AF)',
         'Annualized Revenue (AR)', 'TVL', 'TVL Turnover ' + str(30) + ' days', 'Token Price', 'Realized Volatility %', 'Market Cap (MC)', 'Fully Diluted Valuation (FDV)',
              'MC / AF', 'FDV / AF', 'MC / AR', 'FDV / AR', 
              'MC / TVL', 'FDV / TVL']
        data = [daily_avg_volume, annualized_volume, annualized_fees, 
            annualized_revenue, tvl_current, tvl_turnover, token_price, realized_volatility, mc, fdv, 
            mc_af, fdv_af, mc_ar, fdv_ar, mc_tvl, fdv_tvl]
        table = pd.DataFrame(data = data, index = titles, columns=[f'{project_id}'])
        table.loc[:, f"{project_id}"] =table[f"{project_id}"].map('{:,.4f}'.format)
        df_list.append(table)
    result = pd.concat(df_list, axis=1)   
    return result

def multi_projects_price(project_ids, start_date):
    """
    This is a Python function named "multi_projects_price" that takes in two arguments: a list of project IDs and a start date.
    The function retrieves price data for each project ID and generates a line plot of the prices over time.
    The function returns the resulting plot as a matplotlib Figure object.

    Example usage:

      from multi_project_price import multi_project_price
      project_ids = ['bitcoin', 'ethereum']
      start_date = '2022-01-01'
      result = multi_project_price(project_ids, start_date)

    """

    def get_data(data):
        date = []
        price = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            price.append(data[i]['price'])
        dataa = [price]
        df = pd.DataFrame(dataa, columns=date, index=['price'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['price'].plot(color='crimson', ax=ax, label=f'{project_id} price')
        else:
            df['price'].plot(color=f'C{i}', ax=ax, label=f'{project_id} price')

    ax.set_title("Prices of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Price', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_fdv(project_ids, start_date):

    """
      This is a Python function named "multi_projects_fdv" that takes in two arguments: a list of project IDs and a start date.
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
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['fdv'].plot(color='crimson', ax=ax, label=f'{project_id} fdv')
        else:
            df['fdv'].plot(color=f'C{i}', ax=ax, label=f'{project_id} fdv')

    ax.set_title("FDV of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('FDV', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_mcap(project_ids, start_date):

    """
      This is a Python function named "multi_projects_mcap" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves mcap data for each project ID and generates a line plot of the mcap over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_mcap import multi_project_mcap
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_mcap(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        mcap = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            mcap.append(data[i]['market_cap_circulating'])
        dataa = [mcap]
        df = pd.DataFrame(dataa, columns=date, index=['mcap'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_circulating"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['mcap'].plot(color='crimson', ax=ax, label=f'{project_id} mcap')
        else:
            df['mcap'].plot(color=f'C{i}', ax=ax, label=f'{project_id} mcap')

    ax.set_title("MCAP of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('MCAP', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_tvl(project_ids, start_date):

    """
      This is a Python function named "multi_projects_tvl" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves tvl data for each project ID and generates a line plot of the tvl over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_tvl import multi_project_tvl
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_tvl(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        tvl = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            tvl.append(data[i]['tvl'])
        dataa = [tvl]
        df = pd.DataFrame(dataa, columns=date, index=['tvl'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tvl"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['tvl'].plot(color='crimson', ax=ax, label=f'{project_id} tvl')
        else:
            df['tvl'].plot(color=f'C{i}', ax=ax, label=f'{project_id} tvl')

    ax.set_title("TVL of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('TVL', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_fees(project_ids, start_date):

    """
      This is a Python function named "multi_projects_fees" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves fees data for each project ID and generates a line plot of the fees over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_fees import multi_project_fees
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_fees(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        fees = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            fees.append(data[i]['fees'])
        dataa = [fees]
        df = pd.DataFrame(dataa, columns=date, index=['fees'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=fees"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['fees'].plot(color='crimson', ax=ax, label=f'{project_id} fees')
        else:
            df['fees'].plot(color=f'C{i}', ax=ax, label=f'{project_id} fees')

    ax.set_title("FEES of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('FEES', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_revenue(project_ids, start_date):

    """
      This is a Python function named "multi_projects_revenue" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves revenue data for each project ID and generates a line plot of the revenue over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_revenue import multi_project_revenue
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_revenue(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        revenue = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            revenue.append(data[i]['revenue'])
        dataa = [revenue]
        df = pd.DataFrame(dataa, columns=date, index=['revenue'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=revenue"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['revenue'].plot(color='crimson', ax=ax, label=f'{project_id} revenue')
        else:
            df['revenue'].plot(color=f'C{i}', ax=ax, label=f'{project_id} revenue')

    ax.set_title("Revenue of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Revenue', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_active_dev(project_ids, start_date):

    """
      This is a Python function named "multi_projects_active_dev" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves active developoers number data for each project ID and generates a line plot of the data over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_active_dev import multi_project_active_dev
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_active_dev(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        active_dev = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            active_dev.append(data[i]['active_developers'])
        dataa = [active_dev]
        df = pd.DataFrame(dataa, columns=date, index=['active_developers'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=active_developers"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['active_developers'].plot(color='crimson', ax=ax, label=f'{project_id} active developers')
        else:
            df['active_developers'].plot(color=f'C{i}', ax=ax, label=f'{project_id} active developers')

    ax.set_title("active developers of Multiple Tokens", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('active developers', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def multi_projects_code_commits(project_ids, start_date):

    """
      This is a Python function named "multi_projects_code_commits" that takes in two arguments: a list of project IDs and a start date.
      The function retrieves code commits data for each project ID and generates a line plot of the data over time.
      The function returns the resulting plot as a matplotlib Figure object.

      Example usage:

        from multi_project_code_commits import multi_project_code_commits
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multi_project_code_commits(project_ids, start_date)
        
      """
    def get_data(data):
        date = []
        code_commits = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            code_commits.append(data[i]['code_commits'])
        dataa = [code_commits]
        df = pd.DataFrame(dataa, columns=date, index=['code_commits'])
        df = df.T.dropna()
        return df
    
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    
    fig, ax = plt.subplots(figsize=(24, 14))
    
    for i, project_id in enumerate(project_ids):
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=code_commits"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        df = get_data(data)
        df = df[f'{start_date}':]
        
        if i == 0:
            df['code_commits'].plot(color='crimson', ax=ax, label=f'{project_id} code commits')
        else:
            df['code_commits'].plot(color=f'C{i}', ax=ax, label=f'{project_id} code commits')

    ax.set_title("code commits of Multiple projects", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('code commits', fontsize=18)
    ax.legend(loc='upper left', fontsize=14)
    ax.legend(loc='upper right', fontsize=14)

    return fig

def fdv_active_dev_ratio(project_id, start_date):

    """
    Retrieves the historical data for a given project ID from the Token Terminal API, computes the ratio between
    the project's fully diluted valuation (FDV) and the number of active developers, and plots the result as a time
    series chart. The chart shows the weekly value of the ratio from the given start date until the present, and
    includes a text annotation with the current value of the ratio.

    :param project_id: A string representing the project ID to retrieve data for.
    :param start_date: A string representing the start date of the analysis in ISO format (e.g., '2022-01-01').
    :return: A Matplotlib Figure object representing the chart.

    Example usage:

        from fdv_active_dev_ratio import fdv_active_dev_ratio
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = fdv_active_dev_ratio(project_ids, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data(data):
        date = []
        FDV = []
        active_dev = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            FDV.append(data[i]['market_cap_fully_diluted'])
            active_dev.append(data[i]['active_developers'])
        dataa = [FDV, active_dev]
        df = pd.DataFrame(dataa, columns=date, index=['FDV', 'active_dev'])
        df = df.T.dropna()
        return df

    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=active_developers%2Cmarket_cap_fully_diluted"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    d = get_data(data)
    d = d[::-1]
    d['fdv/active_dev'] = d['FDV']/d['active_dev']
    d = d[f'{start_date}':]
        # Resample the data to weekly frequency
    d_weekly = d.resample('W').last()

    fig, ax = plt.subplots(figsize=(30, 12))
    ax.plot(d_weekly["fdv/active_dev"], label="fdv/active_dev")

        # Get the current value of tvl/ss_fees
    current_value = d_weekly["fdv/active_dev"].iloc[-1]

        # Add current value as text to the plot
    ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

    ax.set_title(f"{project_id} FDV and active developers ratio from {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=18)
    return fig

def fdv_code_commits_ratio(project_id, start_date):

    """
    Retrieves the historical data for a given project ID from the Token Terminal API, computes the ratio between
    the project's fully diluted valuation (FDV) and the number of code commits, and plots the result as a time
    series chart. The chart shows the weekly value of the ratio from the given start date until the present, and
    includes a text annotation with the current value of the ratio.

    :param project_id: A string representing the project ID to retrieve data for.
    :param start_date: A string representing the start date of the analysis in ISO format (e.g., '2022-01-01').
    :return: A Matplotlib Figure object representing the chart.

    Example usage:

        from fdv_code_commits_ratio import fdv_code_commits_ratio
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = fdv_code_commits_ratio(project_ids, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data(data):
        date = []
        FDV = []
        code_commits = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            FDV.append(data[i]['market_cap_fully_diluted'])
            code_commits.append(data[i]['code_commits'])
        dataa = [FDV, code_commits]
        df = pd.DataFrame(dataa, columns=date, index=['FDV', 'code_commits'])
        df = df.T.dropna()
        return df

    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Ccode_commits"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    d = get_data(data)
    d = d[::-1]
    d['fdv/code_commits'] = d['FDV']/d['code_commits']
    d = d[f'{start_date}':]
        # Resample the data to weekly frequency
    d_weekly = d.resample('W').last()

    fig, ax = plt.subplots(figsize=(30, 12))
    ax.plot(d_weekly["fdv/code_commits"], label="fdv/code_commits")

        # Get the current value of tvl/ss_fees
    current_value = d_weekly["fdv/code_commits"].iloc[-1]

        # Add current value as text to the plot
    ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

    ax.set_title(f"{project_id} FDV and code commits ratio from {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=18)
    return fig

def fdv_active_users_ratio(project_id, start_date):

    """
    Retrieves the historical data for a given project ID from the Token Terminal API, computes the ratio between
    the project's fully diluted valuation (FDV) and the number of active users, and plots the result as a time
    series chart. The chart shows the weekly value of the ratio from the given start date until the present, and
    includes a text annotation with the current value of the ratio.

    :param project_id: A string representing the project ID to retrieve data for.
    :param start_date: A string representing the start date of the analysis in ISO format (e.g., '2022-01-01').
    :return: A Matplotlib Figure object representing the chart.

    Example usage:

        from fdv_active_users_ratio import fdv_active_users_ratio
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = fdv_active_users_ratio(project_ids, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data(data):
        date = []
        FDV = []
        active_users = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            FDV.append(data[i]['market_cap_fully_diluted'])
            active_users.append(data[i]['active_users'])
        dataa = [FDV, active_users]
        df = pd.DataFrame(dataa, columns=date, index=['FDV', 'active_users'])
        df = df.T.dropna()
        return df

    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Cactive_users"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    d = get_data(data)
    d = d[::-1]
    d['fdv/active_users'] = d['FDV']/d['active_users']
    d = d[f'{start_date}':]
        # Resample the data to weekly frequency
    d_weekly = d.resample('W').last()

    fig, ax = plt.subplots(figsize=(30, 12))
    ax.plot(d_weekly["fdv/active_users"], label="fdv/active_users")

        # Get the current value of tvl/ss_fees
    current_value = d_weekly["fdv/active_users"].iloc[-1]

        # Add current value as text to the plot
    ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

    ax.set_title(f"{project_id} FDV and active users ratio from {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=18)
    return fig

def multiple_projects_performance(project_ids, start_date, entry_money):

    """
    This function takes a list of project ids, a start date and an entry investment amount as input.
    It uses the Token Terminal API to retrieve historical price data for each project and calculates
    the relative performance of the entry investment amount over time for each project.
    The function returns a plot of the relative performance of the entry investment amount in each project.
    
    Args:
    - project_ids: list - a list of project ids for which to retrieve price data
    - start_date: str - the start date of the analysis in 'YYYY-MM-DD' format
    - entry_money: float - the amount of money to invest initially in each project
    
    Returns:
    - matplotlib.figure.Figure - a plot of the relative performance of the entry investment amount in each project

     Example usage:

        from multiple_projects_performance import multiple_projects_performance
        project_ids = ['bitcoin', 'ethereum']
        start_date = '2022-01-01'
        result = multiple_projects_performance(project_ids, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def standardize(data, start_value):
        data.iloc[0] = start_value
        
        for i in range(1, len(data)):
            data.iloc[i] = data.iloc[i-1] * np.exp(data.iloc[i])
        
        return data

    def get_data(data):
        date = []
        price = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            price.append(data[i]['price'])
        dataa = [price]
        df = pd.DataFrame(dataa, columns=date, index=['price'])
        df = df.T.dropna()
        return df

    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

    d_list = []
    for project_id in project_ids:
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        d = get_data(data)
        d = d[::-1]
        d_CCR = (np.log(d)-np.log(d.shift(1)))[1:]
        #d_CCR = d_CCR.iloc[::-1]
        d_stand = standardize(d_CCR['price'][((d_CCR.index.year >= start_date.year) & (d_CCR.index.month >= start_date.month) & (d_CCR.index.day >= start_date.day)) | (d_CCR.index.year > start_date.year)], start_value=entry_money)
        d_list.append(d_stand)

    stand = pd.concat(d_list, axis=1, keys=project_ids)

    fig, ax = plt.subplots(figsize=(24, 14))
    stand.plot(ax=ax)

    ax.set_title(f"Relative performance of ${entry_money} invested in {len(project_ids)} projects at {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Balance', fontsize=18)
    return fig

def fees_tvl_ratio(project_id, start_date):

    """
    This function takes in a project ID and a start date, and retrieves data on the total value locked (TVL),
    fees, and revenue for the given project from the Token Terminal API. It then calculates the "ss fees" (i.e.
    the fees earned by the project's stakers after accounting for revenue sharing), and computes the ratio of
    supply side fees to TVL. The resulting time series is plotted, along with the current value of the ratio, as a function
    of time. The function returns a matplotlib figure object.

    Example usage:

        from fees_tvl_ratio import fees_tvl_ratio
        project_ids = 'bitcoin'
        start_date = '2022-01-01'
        result = fees_tvl_ratio(project_id, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data(data):
        date = []
        TVL = []
        fees = []
        revenue = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            TVL.append(data[i]['tvl'])
            fees.append(data[i]['fees'])
            revenue.append(data[i]['revenue'])
        dataa = [TVL, fees, revenue]
        df = pd.DataFrame(dataa, columns=date, index=['TVL', 'fees', 'revenue'])
        df = df.T.dropna()
        return df

    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=tvl%2Cfees%2Crevenue"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    d = get_data(data)
    d = d[::-1]
    d['ss fees'] = d['fees'] - d['revenue']
    d['ss fees'] = d['ss fees'].rolling(30).sum().dropna()
    d['ss fees'] = d['ss fees'] * (365 / 30)
    d['ss_fees/tvl'] = d['ss fees']/d['TVL']
    d = d[f'{start_date}':]
        # Resample the data to weekly frequency
    d_weekly = d.resample('W').last()

    fig, ax = plt.subplots(figsize=(30, 12))
    ax.plot(d_weekly["ss_fees/tvl"], label="ss_fees/tvl")

        # Get the current value of tvl/ss_fees
    current_value = d_weekly["ss_fees/tvl"].iloc[-1]

        # Add current value as text to the plot
    ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

    ax.set_title(f"{project_id} Fees and TVL ratio from {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=18)
    return fig

def fdv_revenue_ratio_and_fdv(project_id, start_date):

    """
    This function takes a project ID and start date as inputs and retrieves fully diluted market cap
    and revenue data for the project using the Token Terminal API.
    It then calculates the FDV/revenue ratio and FDV values, and plots them on a graph. The function resamples the data to weekly frequency,
    calculates the current value of the FDV/revenue ratio, and adds it to the plot as text.
    The resulting plot shows the FDV and FDV/revenue ratio trends over time for the given project.

    Example usage:

        from fdv_revenue_ratio_and_fdv import fdv_revenue_ratio_and_fdv
        project_id = 'bitcoin'
        start_date = '2022-01-01'
        result = fdv_revenue_ratio_and_fdv(project_id, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data(data):
        date = []
        FDV = []
        revenue = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            FDV.append(data[i]['market_cap_fully_diluted'])
            revenue.append(data[i]['revenue'])
        dataa = [FDV, revenue]
        df = pd.DataFrame(dataa, columns=date, index=['FDV', 'revenue'])
        df = df.T.dropna()
        return df

    url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Crevenue"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response = requests.get(url, headers=headers)
    data_shows = json.loads(response.text)
    data = data_shows['data']
    d = get_data(data)
    #d = d['2021-10-15':]
    d = d[::-1]
    d['revenue'] = d['revenue'].rolling(30).sum().dropna()
    d['revenue'] = d['revenue'] * (365 / 30)
    d['FDV/revenue'] = d['FDV']/d['revenue']
    d = d[f'{start_date}':]
        # Resample the data to weekly frequency
    d_weekly = d.resample('W').last()

    fig, ax = plt.subplots(figsize=(30, 12))
    ax2 = ax.twinx()
    ax.plot(d_weekly["FDV/revenue"], label="FDV/revenue",color='crimson')
    ax2.plot(d_weekly["FDV"], label="FDV")
        # Get the current value of tvl/ss_fees
    current_value = d_weekly["FDV/revenue"].iloc[-1]

        # Add current value as text to the plot
    ax.text(d_weekly.index[-1], current_value, f"Current value: {current_value:.2f}", fontsize=16, ha="right", va="top")

    ax.set_title(f"{project_id} FDV and Annualized revenue ratio with FDV from {start_date}", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Ratio', fontsize=18)
    return fig

def market_project_fdv_revenue(project_ids,project_id,start_date):
    """
    A function that retrieves market capitalization, revenue, and fully diluted valuation data
    for a list of projects and a specified project, calculates their respective FDV/Annualized Revenue ratios,
    and plots the results on a graph.

    Args:
        project_ids (list of str): A list of project names to retrieve data for and that projects represent market.
        project_id (str): The name of the project to compare to the market average.
        start_date (str): A string representing the start date of the graph in the format 'yyyy-mm-dd'.

    Returns:
        fig (matplotlib.figure.Figure): A matplotlib figure object displaying the graph.

        Example usage:

        from market_project_fdv_revenue import market_project_fdv_revenue
        project_ids = ['lido-finance','aave',''compound','makerdao']
        project_id = 'dydx'
        start_date = '2022-01-01'
        result = market_project_fdv_revenue(project_ids, project_id, start_date)
    """
    start_date = pd.to_datetime(start_date)
    def get_data1(project_name):
        url = f"https://api.tokenterminal.com/v2/projects/{project_name}/metrics?metric_ids=market_cap_fully_diluted%2Crevenue%2Cmarket_cap_circulating"
        headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        date = []
        fdv = []
        mcap = []
        revenue = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            fdv.append(data[i]['market_cap_fully_diluted'])
            if project_name == "lido-finance":
                if data[i]['revenue'] is not None:
                    revenue.append(data[i]['revenue'] / 2)
                else:
                    revenue.append(None)
            else:
                revenue.append(data[i]['revenue'])
            mcap.append(data[i]['market_cap_circulating'])
        dataa = [fdv,revenue,mcap]
        df = pd.DataFrame(dataa, columns=date, index=['fdv','revenue','mcap'])
        df = df.T.dropna()
        df = df[::-1]
        last_n_days_revenue = df['revenue'].rolling(30).sum()
        annualized_revenue = last_n_days_revenue * (365 / 30)
        df['revenue'] = annualized_revenue
        df['fdv/revenue'] = df['fdv'] / df['revenue']
        return df

    project_names = project_ids
    dfs = [get_data1(name) for name in project_names]

    df = pd.concat(dfs).groupby(level=0).mean()

    def get_data(data):
        date = []
        fdv = []
        revenue = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            fdv.append(data[i]['market_cap_fully_diluted'])
            revenue.append(data[i]['revenue'])
        dataa = [fdv,revenue]
        df = pd.DataFrame(dataa, columns=date, index=['fdv','revenue'])
        df = df.T.dropna()
        return df

    url_pr = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=market_cap_fully_diluted%2Crevenue"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response_pr = requests.get(url_pr, headers=headers)
    data_shows_pr = json.loads(response_pr.text)
    data_pr = data_shows_pr['data']
    d_pr = get_data(data_pr) 
    d_pr = d_pr.iloc[::-1]
    last_n_days_revenue = d_pr['revenue'].rolling(30).sum().dropna()
    annualized_revenue = last_n_days_revenue * (365 / 30)

    # replace the revenue column with the annualized revenue
    d_pr['revenue'] = annualized_revenue

    d_pr['fdv/revenue'] = d_pr['fdv'] / d_pr['revenue']

    fig, ax = plt.subplots(figsize=(24, 14))
    ax2 = ax.twinx()
    d_pr['fdv/revenue'][f'{start_date}':].plot(color='crimson', ax=ax)
    df['fdv/revenue'][f'{start_date}':].plot(color='green', ax=ax2)
    # convert the date string to a datetime object
    crash_date = pd.to_datetime('2022-11-10 00:00:00+00:00')

    # convert the datetime object to a numeric format
    crash_date_num = mdates.date2num(crash_date)

    ax.axvline(x=crash_date, color='black', linestyle='--', alpha=0.9)
    ax.text(crash_date, 11, 'FTX crash', rotation=90, ha='right', fontsize=14, va='top', fontweight='bold')

    ax.set_title(f"Market Mean FDV/Annualized Revenue and {project_id} FDV/Annualized Revenue Ratio", fontsize=18)
    ax.set_xlabel('Date', fontsize=18)
    ax2.set_ylabel(f'{project_id} FDV/Annualized Revenue Ratio', color='crimson', fontsize=20)
    ax.set_ylabel('Market Mean FDV/Annualized Revenue Ratio', color='green', fontsize=20)
    return fig

def project_df_2(project_id):
    """
    This function retrieves metrics data for cryptocurrency project from an API and
    creates a dataframe with various financial metrics for project.
    It takes a project_id as input and returns a pandas dataframe with financial metrics such as:
    Volume, Fees, Fees %, Incentive, Fees/Incentives ratio, Non-subsidized revenue, Non-subsidized volume

    To use this function, import it into your python script and call it with a project_id as an argument.
    The resulting dataframe can be used for financial analysis.

    Example usage:

    from project_df_2 import project_df_2
    project_id = 'bitcoin'
    result = project_df_2(project_id)

    """
    def get_data(data):
      date = []
      volume = []
      fees = []
      incentives = []
      for i in range(len(data)):
          date.append(pd.to_datetime((data[i]['timestamp'])))
          volume.append(data[i]['trading_volume'])
          fees.append(data[i]['fees'])
          incentives.append(data[i]['token_incentives'])
      dataa = [volume,fees,incentives]
      df = pd.DataFrame(dataa, columns=date, index=['volume','fees','incentives'])
      df = df.T.dropna()
      return df

    url_d = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=trading_volume%2Cfees%2Ctoken_incentives"
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
    response_d = requests.get(url_d, headers=headers)
    data_shows_d = json.loads(response_d.text)
    data_d = data_shows_d['data']
    d_d = get_data(data_d)  
    d_d = d_d[::-1]
    def pr_30_days(df):

      volume_30_days = np.average(df.iloc[-30:]['volume'])/1e9
      volume_30_days_ = f'{volume_30_days:.2f}'
      volume_annualized = (volume_30_days*365)
      volume_annualized_ = f'{volume_annualized:.2f}'
      fees_30_days = np.average(df.iloc[-30:]['fees'])/1e6
      fees_30_days_ = f'{fees_30_days:.2f}'
      fees_annualized = fees_30_days*365
      fees_annualized_ = f'{fees_annualized:.2f}'
      fee_pct = fees_30_days/volume_30_days*100/1000
      fee_pct_ = f'{fee_pct:.5f}'
      incentive_30_days = np.average(df.iloc[-30:]['incentives'])/1e6
      incentive_30_days_ = f'{incentive_30_days:.2f}'
      incentive_annualized = incentive_30_days*365
      incentive_annualized_ = f'{incentive_annualized:.2f}'
      fees_incentives_ratio = fees_30_days/incentive_30_days
      fees_incentives_ratio_ = f'{fees_incentives_ratio:.8f}'
      non_subsidized_revenue = (fees_30_days - incentive_30_days)*1e6
      non_subsidized_revenue_ = f'{non_subsidized_revenue:.2f}'
      non_subsidized_revenue_annualized = (non_subsidized_revenue*365)/1e6
      non_subsidized_revenue_annualized_ = f'{non_subsidized_revenue_annualized:.2f}'
      non_subsidized_volume = (non_subsidized_revenue*100/fee_pct)/1e6
      non_subsidized_volume_ = f'{non_subsidized_volume:.4f}'
      non_subsidized_volume_annualized = (non_subsidized_volume*365)/1e3
      non_subsidized_volume_annualized_ = f'{non_subsidized_volume_annualized:.2f}'

      col = ['Average Daily', 'Annualized']
      rows = ['Volume', 'Fees', 'Fees %', 'Incentive', 'Fees/Incentives', 'Non-subsidized revenue', 'Non-subsidized volume']
                  
      data = [{'Average Daily':volume_30_days_+' B','Annualized':volume_annualized_+'B'}, 
              {'Average Daily':fees_30_days_+' M','Annualized':fees_annualized_+'M '}, 
              {'Average Daily':fee_pct_,'Annualized':' '},
              {'Average Daily':incentive_30_days_+' M','Annualized':incentive_annualized_+' M'},
              {'Average Daily':'    '+fees_incentives_ratio_,'Annualized':'      '},
              {'Average Daily':non_subsidized_revenue_,'Annualized':non_subsidized_revenue_annualized_+' M'},
              {'Average Daily':non_subsidized_volume_+' M','Annualized':non_subsidized_volume_annualized_+' B'}
              ]
      return pd.DataFrame(data = data, index = rows, columns=col)

    df = pr_30_days(d_d)
    return df

def cor_matrix(project_ids,start_time):
  """
    Calculates the correlation matrix between the daily price data of the given projects.
    
    Parameters:
    project_ids (list): A list of strings representing the IDs of the projects to be included in the correlation matrix.
    start_time (str): A string representing the start date (in format yyyy-mm-dd) for which the price data will be retrieved.
    
    Returns:
    fig: A matplotlib figure object that displays the correlation matrix as a heatmap.

    Example usage:

    from cor_matrix import cor_matrix
    project_ids = ['bitcoin','ethereum','makerdao']
    start_time = '2022-01-01'
    result = cor_matrix(project_ids,start_time)
    """

  start_time = pd.to_datetime(start_time)
  def get_data1(project_name):
      url = f"https://api.tokenterminal.com/v2/projects/{project_name}/metrics?metric_ids=price"
      headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}
      response = requests.get(url, headers=headers)
      data_shows = json.loads(response.text)
      data = data_shows['data']
      date = []
      price = []
      for i in range(len(data)):
          date.append(pd.to_datetime((data[i]['timestamp'])))
          price.append(data[i]['price'])
      dataa = [price]
      df = pd.DataFrame(dataa, columns=date, index=[f'{project_name}'])
      df = df.T.dropna()
      df = df[::-1]
      df = df[f'{start_time}':]
      return df

  project_names = project_ids
  dfs = [get_data1(name) for name in project_names]

  table = pd.concat(dfs,axis=1)

  matrix = table.corr().round(2)
  fig, ax = plt.subplots(figsize=(12,12))         # Sample figsize in inches
  sns.heatmap(matrix, annot=True, linewidths=.5, ax=ax)
  return fig

def ann_vol_order(project_ids):
    """
    This function takes a list of project IDs as input and returns a bar chart showing the projects
    ordered by their annualized volatility. The function fetches daily price data for each project
    from the Token Terminal API and calculates the annualized volatility based on the last 365 days
    of price data. The bar chart shows the volatility values for each project, with the projects
    ordered from lowest to highest volatility.

    Parameters:
    - project_ids: a list of strings representing the project IDs to include in the chart

    from ann_vol_order import ann_vol_order
    project_ids = ['bitcoin','ethereum','makerdao']
    result = ann_vol_order(project_ids)
    """
    def get_data(data):
        date = []
        price = []
        for i in range(len(data)):
            date.append(pd.to_datetime((data[i]['timestamp'])))
            price.append(data[i]['price'])
            dataa = [price]
            df = pd.DataFrame(dataa, columns=date, index=['price'])
            df = df.T.dropna()
        return df
        
    headers = {"Authorization": "Bearer 3365c8fd-ade3-410f-99e4-9c82d9831f0b"}

    vol = {}
    for project_id in project_ids:
        url = f"https://api.tokenterminal.com/v2/projects/{project_id}/metrics?metric_ids=price"
        response = requests.get(url, headers=headers)
        data_shows = json.loads(response.text)
        data = data_shows['data']
        d = get_data(data)
        d = d[::-1]
        d_CCR = (np.log(d)-np.log(d.shift(1)))[1:].dropna()
        Ann_volatility = np.std(d_CCR[-365:])*np.sqrt(365)*100
        vol[project_id] = Ann_volatility['price']


    sorted_data = sorted(vol.items(), key=lambda x: x[1])

        # Extract the keys and values from the sorted dictionary
    keys = [x[0] for x in sorted_data]
    values = [x[1] for x in sorted_data]

    a = plt.figure(figsize=(20, 15))

        # Plot the bar plot
    plt.bar(keys, values)
    plt.xlabel('Project',fontsize=20)
    plt.ylabel('Volatility',fontsize=20)
    plt.title('Projects order by annualized volatility',fontsize=20)

    return a


