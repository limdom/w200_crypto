import json
from datetime import date
import numpy as np
import pandas as pd

def flat_sand_data(file_name):
    
    """Flatten JSON object to derive transaction level data."""
    
    with open(file_name,'r') as json_file:
        json_data = json.load(json_file)
        df = pd.json_normalize(
            json_data,
            record_path=["holders","transactions"],
            sep="_",
            meta=[
                     ['holders','address'],
                     ['holders','balance'],
                     ['holders','share'],
                     ['holders','tag']
            ],
            errors='ignore'
        )
        df = df.rename(
            columns={
                'type': 'tx_type',
                'from': 'address_from',
                'to': 'address_to',
                'value': 'abs_value'
            }
        )
        
        df = df.reindex(
            columns = [
                'holders_address',
                'holders_balance', 
                'holders_share',
                'holders_tag',
                'transactionHash',
                'timestamp',
                'tx_type',
                'address_from',
                'address_to',
                'abs_value',
                'USD_price_at_timestamp',
            ]
        )
        
    return df

def make_readible(df):
    
    """ df_tx takes a copy of df_no_tag and makes for better readability. EXCLUDES tagged wallets."""

    readible_df = df.copy()

    readible_df['uniq_transID'] = readible_df[['holders_address','timestamp']].apply(lambda x: '_'.join(x.values.astype(str)), axis=1)
    readible_df['date_time'] = pd.to_datetime(readible_df['timestamp'], unit='s') # Convert from UNIX timestamp.
    readible_df['value'] = np.where(readible_df['holders_address']!=readible_df['address_from'], -readible_df['abs_value'],
    readible_df['abs_value']) # Positive values are sales, Negative values indicate purchase.
    readible_df['value_in_USD'] = readible_df['value'] * readible_df['USD_price_at_timestamp'] # Cash Flow data in USD.
    
    return readible_df


def aggregate_wallet(df1, df2):
    
    """ wallet_level_data (df): this should provide a wallet-level dataframe to house investment return data.
    We are choosing df_flat which still has the UNIX timestamp."""

    df_merge = pd.DataFrame(
        df1[
                ["holders_address",
                "timestamp",
            ]
        ]
        .groupby(["holders_address"])
        .min(numeric_only=True)
    )

    df_merge.insert(loc=0, column='row_num', value=np.arange(len(df_merge)))
    df_merge['row_num'] = df_merge.reset_index(inplace=True)
    df_merge.drop(['row_num'], axis=1, inplace=True)
    df_merge['uniq_transID'] = df_merge[['holders_address','timestamp']].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
    df_merge = df_merge.rename(columns={'transactionHash': 'initial_tx_hash',})

    df_merge = pd.merge(df_merge, df2, on="uniq_transID",how='inner')
    df_merge['holding_period_days'] = (pd.Timestamp(date.today()) - df_merge['date_time']).astype('timedelta64[D]')
    df_merge.drop(['holders_address_y','timestamp_y','timestamp_x'], axis=1, inplace=True)

    df_merge.rename(
                columns={
                    'holders_address_x': 'holders_address',
                    'holders_balance_x': 'holders_balance',
                    'abs_value': 'inital_abs_value',
                    'date_time': 'initial_dt',
                    'value': 'initial_value',
                    'value_in_USD': 'initial_value_in_USD'
                },
            inplace = True
        )

    df_merge = df_merge[['holders_address','USD_price_at_timestamp','inital_abs_value','initial_dt','initial_value','initial_value_in_USD','holding_period_days']]

    return df_merge

def collapse_initial(df):
    
    """Takes an inital dataframe (df) and collapses all initial transactions for wallet holders that have multiple initial transactions."""
    
    new_df = df.groupby('holders_address').first()
    
    holders_count = dict(df['holders_address'].value_counts())
    multi_list = [x for x in holders_count if holders_count[x]>1]
    
    # Aggregates all instances of initial_abs_value, initial_value, initial_value_in USD.
    for wallet in multi_list:
        multi_genesis = df[df['holders_address'] == wallet]
        multi_genesis = multi_genesis[['inital_abs_value','initial_value','initial_value_in_USD']].sum()
        
        new_df.at[wallet,'inital_abs_value'] = multi_genesis[0]
        new_df.at[wallet,'initial_value'] = multi_genesis[1]
        new_df.at[wallet,'initial_value_in_USD'] = multi_genesis[2]

    new_df.reset_index() 
    
    
    return new_df
