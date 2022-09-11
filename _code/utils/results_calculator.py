# import OS module
from cgi import print_form
from cmath import inf
from operator import le
import os
from time import time
import pandas as pd
import numpy as np
# This is my path

def calculate(df:pd.DataFrame,metaData):
    ticker,timeframe,tp,sl,year=metaData['ticker'],metaData['timeframe'],metaData['tp'],metaData['sl'],metaData['year']
    res_df = pd.DataFrame(columns=['ticker', 'timeframe', 'positions_Count', 'total_profit/loss', 'tp_count', 'sl_count',
                            'tc_count', 'long', 'win_long', 'short', 'win_short','TC','win_TC', 'max_win', 'max_loss'])

    buies = df.where(df['type'] == 'Buy').dropna()
    all_buies=len(buies)

    buy_tp_count = buies.where(buies['closetype'] == 'tp').count()[0]
    buy_sl_count = buies.where(buies['closetype'] == 'sl').count()[0]
    buy_tc_count = buies.where(buies['closetype'] == 'TC').count()[0]
    buy_tp_sum = buies['p/l'].where(buies['closetype'] == 'tp').sum()
    buy_sl_sum = buies['p/l'].where(buies['closetype'] == 'sl').sum()
    buy_tc_sum = buies['p/l'].where(buies['closetype'] == 'TC').sum()
    
    
    sells = df.where(df['type'] == 'Sell').dropna()
    all_sells=len(sells)

    sell_tp_count = sells.where(sells['closetype'] == 'tp').count()[0]
    sell_sl_count = sells.where(sells['closetype'] == 'sl').count()[0]
    sell_tc_count = sells.where(sells['closetype'] == 'TC').count()[0]
    sell_tp_sum = sells['p/l'].where(sells['closetype'] == 'tp').sum()
    sell_sl_sum = sells['p/l'].where(sells['closetype'] == 'sl').sum()
    sell_tc_sum = sells['p/l'].where(sells['closetype'] == 'TC').sum()

    tc_all_sum = sell_tc_sum+buy_tc_sum
    sl_all_sum = sell_sl_sum+buy_sl_sum
    tp_all_sum = sell_tp_sum+buy_tp_sum
    total_profit = tc_all_sum+sl_all_sum+tp_all_sum

    # tc_count=df.where(df['closetype']=='TC').count()[0]
    # sl_times=df.where(df['closetype']=='sl').count()[0]
    # tp_times=df.where(df['closetype']=='tp').count()[0]
    max_win = df['p/l'].max()
    max_loss = df['p/l'].min()
    # total_profit=df['AccPL'].iloc[-1]

    data = {
        'ticker': ticker, 'timeframe': timeframe,
        'positions_Count': all_buies+all_sells,
        'tp_count':buy_tp_count+sell_tp_count,
        'sl_count':buy_sl_count+sell_sl_count,
        'tc_count':buy_tc_count+sell_tc_count, 
        'long':{'c':round(all_buies,2),'s':round(buy_tp_sum+buy_sl_sum+buy_tc_sum,2)},
        'short':{'c':round(all_sells,2),'s':round(sell_tp_sum+sell_sl_sum+sell_tc_sum,2)},
        'TC':{'c':buy_tc_count+sell_tc_count,'s':round(tc_all_sum,2)},
        'win_long':[buy_tp_count,buy_sl_count,buy_tc_count], 
        'win_short':[sell_tp_count,sell_sl_count,sell_tc_count],
        'win_TC':[None,None,sell_tc_count+buy_tc_count,round(tc_all_sum,2)],
        'max_win':max_win, 'max_loss':max_loss, 
        'total_profit/loss':round(total_profit,2)
        }

    res_df=res_df.append(data,ignore_index=True)

    return res_df
# res_df.to_csv(f'{path}/{year}-Total_results_data.csv')
# print(res_df)