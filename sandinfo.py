#!/usr/bin/env python
# coding: utf-8


# pip install pycoingecko
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import pandas as pd
from pycoingecko import CoinGeckoAPI
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')



# Enter in datetime in %Y-%m-%d format
def set_timeframe(startdate, enddate):
    
    """Use this function to set a timeframe and convert it into a UNIX format. 
    The output is a list with the first element as the start date and the 
    second element is the end date."""

    startdate_unix = time.mktime(datetime.strptime(startdate, '%Y-%m-%d').timetuple())
    enddate_unix = time.mktime(datetime.strptime(enddate, '%Y-%m-%d').timetuple())
    
    return [startdate_unix, enddate_unix]


def get_sand_returns(timeframe):
    
    """Input a timeframe that is in a list format to pull the historical price,
    market cap, and total volume data from the Coin Gecko API for $SAND within
    the specified time range. The output is a dataframe with 4 columns: date,
    price, market cap, and total volume."""
    
    startdate_unix = timeframe[0]
    enddate_unix = timeframe[1]
    
    cg = CoinGeckoAPI()
    
    # Pulling historical data of $SAND from coingecko API based on the specified date range
    date_price = cg.get_coin_market_chart_range_by_id(id='the-sandbox',vs_currency='usd',
                                         from_timestamp=startdate_unix,
                                         to_timestamp=enddate_unix)

    # date_price dictionary containing three keys: prices, market_caps, total_volumes
    date_p_df = pd.DataFrame(date_price['prices'],columns = ['date','prices'])
    date_mc_df = pd.DataFrame(date_price['market_caps'],columns = ['date','market_caps'])
    date_v_df = pd.DataFrame(date_price['total_volumes'],columns = ['date','total_volumes'])

    date_p_mc_df = pd.merge(date_p_df, date_mc_df, on='date')
    date_merged_df = pd.merge(date_p_mc_df, date_v_df, on='date')

    
    # Converting date from UNIX to datetime
    date_merged_df['date'] = pd.to_datetime(date_merged_df['date'], unit='ms').apply(lambda x: x.to_datetime64())
    
    
    # Calculating local minimum and maximum
    date_merged_df['prices'].to_numpy()
    date_merged_df['min'] = date_merged_df.iloc[argrelextrema(date_merged_df['prices'].to_numpy(), np.less_equal,
                    order=1)]['prices']
    date_merged_df['max'] = date_merged_df.iloc[argrelextrema(date_merged_df['prices'].to_numpy(), np.greater_equal,
                    order=1)]['prices']
    
    return date_merged_df




def sand_price_volume_plot(date_merged_df):
    
    """Graph $SAND price and volume data on a line chart using Matplotlib."""

    # Plot the historical price data
    line_data = date_merged_df.sort_values('date')

    x = line_data['date']
    yp = line_data['prices']
    yv = line_data['total_volumes']
    ymin = line_data['min']
    ymax = line_data['max']

    # Graph historical price
    plt.subplots(figsize=(15,10))
    plt.plot(x, yp, 'b', label = 'daily price')
    plt.title("Historical Price of $SAND and Total Volume Traded, 2020-08-06 to 2021-12-01", fontsize=20)
    plt.xlabel('Date', fontsize=20)
    plt.ylabel('Price in USD', color='b', fontsize=15)
    
    # Annotate the plot with data call out
    arrowprops = dict(arrowstyle = "->",connectionstyle = "angle, angleA = 0, angleB = 120, rad = 10")
    plt.annotate("10-28-2021 \nSpike in trading activity\nafter Meta changed its name", xy =(x[440], 0.95),
                xytext = (x[250],2), size='x-large',
                arrowprops = arrowprops,)

    # Graph historical total volume traded
    plt.gca().twinx().plot(x, yv, 'violet', label = 'daily volume')
    plt.xticks(rotation='vertical')
    plt.ylabel('Volume in USD (billion)', color='m', fontsize=15)
    
    
    plt.show()
    
    
def sand_mm_plot(date_merged_df):
    """Graph $SAND price and volume data on a line chart with
    the local maximum and minimum."""

    # Plot the historical price data
    line_data = date_merged_df.sort_values('date')

    x = line_data['date']
    yp = line_data['prices']
    yv = line_data['total_volumes']
    ymin = line_data['min']
    ymax = line_data['max']
    

    # Graph historical price
    plt.subplots(figsize=(15,10))
    plt.plot(x, yp, 'b', label = 'daily price')
    plt.scatter(x, ymin, color='r')
    plt.scatter(x, ymax, color='g')
    
    # Annotate the plot with data call out
    arrowprops = dict(arrowstyle = "->",connectionstyle = "angle, angleA = 0, angleB = 120, rad = 10")
    plt.annotate("10-28-2021 \nFacebook becomes Meta", xy =(x[83], 0.95),
                xytext = (x[35],2), size='x-large',
                arrowprops = arrowprops,)

    #Labels
    plt.title("Historical Price of $SAND with Local Extrema, 2021-08-06 to 2021-12-01", fontsize=20)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Price in USD', color='b', fontsize=15)

    
    
def standard_date(date):
    """The function standardizes the date/timestamps so that it outputs as a string
    format without the time"""
    
    return date.strftime('%Y-%m-%d')


def standard_datetime(date):
    """The function standardizes the date/timestamps so that it outputs as a string
    format without the time"""
    
    return date.strftime('%Y-%m-%d %H:%M:%S')



def get_index(start_date, date_merged_df):
    
    """Enter a start_date in a string format. This function uses
    this string to search for the index of that date in the dataframe."""
    
    if datetime.strptime(start_date,'%Y-%m-%d') >= datetime.strptime('2020-08-14','%Y-%m-%d'):
        
        index_list = date_merged_df.index[date_merged_df['date'] == start_date].tolist()
        index = index_list[0]
        
    else:
        index = 0

    return index



def filter_df(index, date_merged_df):
    """This function filters the dataframe to show only the 
    rows at the specified index and below."""
    
    return date_merged_df[index:]
    

    
def sand_volatility(filter_df):
    
    """Calculate Sand volatility by inputting a dataframe containing
    price data of the asset. That time range would serve as the 
    holding period. This function will calculate the returns over 
    that holding period."""
    
    # Calculate log returns of an asset
    filter_df['log_returns'] = np.log(filter_df['prices']/filter_df['prices'].shift())
    
    # Calculate the daily standard deviation of the log returns
    volatility = filter_df['log_returns'].std()*np.sqrt(365)
    
    return volatility
    
    

def waterfall_data(txn_df, holder_address):
    
    """This function will intake the large transactions dataframe
    and the specified holder_address to create the dataframe used
    to generate the graph in graph_waterfall()."""
    

    # Graph waterfall for wallet id 41 for in-flow-out-flow of value_in_USD
    waterfall_df = txn_df[['holders_address','date_time','value_in_USD','value']].sort_values('date_time')
    wallet_txn = waterfall_df.loc[waterfall_df['holders_address']==holder_address]
    wallet_txn['date'] = wallet_txn['date_time'].apply(standard_date)
    wallet_txn['value_in_USD'] = wallet_txn['value_in_USD']*-1
    wallet_txn['value'] = wallet_txn['value']*-1
    wallet_txn_net = wallet_txn.groupby('date').sum().sort_values('date')
    wallet_txn_net = wallet_txn_net.sort_values('date')


    # Create initial df with all columns to create the stacked graph
    wallet_txn_net['cum_sum'] = wallet_txn_net['value_in_USD'].cumsum()
    wallet_txn_net['blank'] = wallet_txn_net['cum_sum'].copy()
    wallet_txn_net['blank'] = wallet_txn_net['blank'].shift(1).fillna(0)
    wallet_txn_net.loc['Net Total'] = [0]*4
    wallet_txn_net['date'] = wallet_txn_net.index.tolist()
    # wallet_txn_net.loc['Current NT'] = [0]*5
    
    return wallet_txn_net



def graph_waterfall(wallet_txn_net, sand_info_df, wallet_id):
    
    """This function takes the df generated from waterfall_data(),
    the historical sand price data, and the name of the wallet_id as inputs.
    The output will graph the net daily transactions made by wallet_id,
    and overlay it with the sand price."""
    
    
    # Intermediate df to graph Increases in value_in_USD
    increases = wallet_txn_net.copy()
    increases['value_in_USD'].loc[increases['value_in_USD'] <0] = 0

    x = increases['date']
    y_increase_value = increases['value_in_USD']
    y_increase_blank = increases['blank']


    # Intermediate df to graph Decreases in value_in_USD
    decreases = wallet_txn_net.copy()
    decreases['value_in_USD'].loc[decreases['value_in_USD'] >0] = 0

    y_decrease_value = decreases['value_in_USD']
    y_decrease_blank = decreases['blank']


    # Calculate the Net Total to graph in plot
    total = wallet_txn_net['value_in_USD'].sum()
    length = len(wallet_txn_net['value_in_USD'])
    y_total = [0]*length
    y_total[-1] = total

    
    # # Graph the current value of Net Total
    # current = wallet_41_daily['value'].sum()*7.23
    # y_current = [0]*length
    # y_current[-1] = current
    # y_current


    # Graph SAND price
    y_sand = []

    for i in wallet_txn_net['date']:
        if i == "Net Total":
            i = wallet_txn_net['date'][-2]
            price = None
       
        else: 
            price = sand_info_df['prices'].loc[sand_info_df['date'] == i].item()
        
        y_sand.append(price)
   
    
    # Plot the stacked bar graph
    plt.xticks(rotation=45)
    plt.bar(x, y_increase_blank, color='white')
    plt.bar(x, y_increase_value, bottom=y_increase_blank, color='green')
    plt.bar(x, y_decrease_blank, color='white')
    plt.bar(x, y_decrease_value, bottom=y_decrease_blank, color='red')
 
    # Plot Net Total
    plt.gca().bar(x, y_total, color = 'b')
    # plt.bar(x, y_current, color = 'b')

    
    # Label stacked bar graph
    plt.title('Trading activity over time for ' + "Wallet 72")
    plt.grid(alpha=0.2)
    plt.ylabel('Value in USD')

    
    # Plot SAND prices and labels
    plt.title('Trading activity over time for ' + wallet_id)
    plt.gca().twinx().plot(x, y_sand, 'c--', label = '$SAND price')
    plt.ylabel('Price in USD')
    plt.legend()
    
    

