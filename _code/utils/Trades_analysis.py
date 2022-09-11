

# filepath='TradesData/SuperTrend/2010/5m/ETHUSDT-5m.csv'

# import OS module

import os
import pandas as pd
import numpy as np
# This is my path






class tradesAnalizer:
    def __init__(self,ticker,timeframe,strategy,period=20,multiplayer=10) -> None:
        self._period=period
        self._multiplayer=multiplayer
        self._ticker=ticker
        self._timeframe=timeframe
        self._stName=strategy['name']
        self._tp=strategy['tp']
        self._sl=strategy['sl']
        self._year=strategy['year']

        self.m1_path = f'Data/2022/{self._ticker}/{self._ticker}-1m.csv'
        self.filePath=f'./TradesData/{self._stName}-{self._period}{self._multiplayer}/{self._year}/{self._timeframe}/{self._ticker}-{self._sl}-{self._tp}.csv'
        self.savePath=f'./TradesData/{self._stName}-{self._period}{self._multiplayer}/{self._year}/{self._timeframe}/analyzed/ANA-{self._ticker}-{self._sl}-{self._tp}.csv'
        self.df = pd.read_csv(self.filePath)

    def fetch_trade_ana(self, trade):
            sub_df1m = self.df_1m.loc[(self.df_1m['open_time'] >= trade.opendate) & 
                                      (self.df_1m['close_time'] <= trade.closedate)]
            # print(sub_df1m.tail(50))
            highest_price=sub_df1m['high'].max()
            lowest_price=sub_df1m['low'].min()
            if trade.type=='Buy':
                perc_lowest=round((lowest_price-trade.openprice)/trade.openprice*100,2)
                perc_highest=round((highest_price-trade.openprice)/trade.openprice*100,2)
            else:
                perc_lowest=round((trade.openprice-lowest_price)/trade.openprice*100,2)
                perc_highest=round((trade.openprice-highest_price)/trade.openprice*100,2)
       
            return [lowest_price,perc_lowest],[highest_price,perc_highest]

    def analize(self):
        
        self.df['opendate']=pd.to_datetime(self.df['opendate'])
        self.df['closedate']=pd.to_datetime(self.df['closedate'])

        
        self.df_1m = pd.read_csv(self.m1_path)
        self.df_1m['open_time']=pd.to_datetime(self.df_1m['open_time'])
        self.df_1m['close_time']=pd.to_datetime(self.df_1m['close_time'])

        self.df['lowest/highest']=self.df.apply(lambda x: self.fetch_trade_ana(x),axis=1)
        self.df['highest']=self.df['lowest/highest'].apply(lambda x: x[1][0])
        self.df['highest%']=self.df['lowest/highest'].apply(lambda x: x[1][1])
        self.df['lowest']=self.df['lowest/highest'].apply(lambda x: x[0][0])
        self.df['lowest%']=self.df['lowest/highest'].apply(lambda x: x[0][1])
        
        self.df=self.df.drop(['number','isclosed','id','qty','size','lowest/highest'],axis=1)
        # print(df.tail(15))
        # df.to_csv(self.savePath)
        return self.df



# year='2021'
# timeframe='5m'

# path = f"TradesData/SuperTrend-2010/{year}/{timeframe}"

# obj = os.scandir(path)
# # res_df = pd.DataFrame(columns=['ticker', 'timeframe', 'sl_tp', 'total_profit/loss', 'tp_count', 'sl_count',
# #                                'tc_times', 'Long', 'win_long', 'short', 'win_short', 'tc_count', 'win_tc', 'max_win', 'max_loss'])
# # print("Files and Directories in '% s':" % path)
# for entry in obj:
#     if entry.is_dir():
#         # get sub dir objects
#         print(entry.name)

#     elif entry.is_file() & ('Total_results_data.csv' not in entry.name) :
#         df = pd.read_csv(entry)
#         info = entry.name.split(sep='-')
#         ticker = info[0]
#         # timeframe = info[1]
#         # sltp = info[3][:2]+'-'+info[3][2:].replace('.csv','')
#         sl = info[1]
#         tp = info[2].replace('.csv','')

        
#         buies = df.where(self.df['type'] == 'Buy').dropna()
#         all_buies=len(buies)
#         str=dict(name='SuperTrend',tp=tp,sl=sl,year=year)
#         ta=tradesAnalizer(ticker=ticker,timeframe=timeframe,strategy=str)
#         ta.analize()