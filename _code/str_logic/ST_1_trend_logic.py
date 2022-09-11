from datetime import datetime
import pandas as pd
from ..utils.stoptake import checkstoploss, checktakeProfit
from ..utils import CSVDataManager as csvMgr
from ..utils import PositionManager as posMgr
from ..models.Positioninfo import Positioninfo
from ..indicators.SuperTrend_indicator import Supertrend


class ST_1_strategy:

    def __init__(self, ticker, timeframe, strategy, period: float, multiplier: float, save,dates) -> None:
        self.start_date,self.end_date=pd.to_datetime(dates['start_date']),pd.to_datetime(dates['end_date'])
        self._year=dates['start_date'].year
        self.save_to_db = save
        self._period = round(period,2)
        self._multiplier = round(multiplier,2)
        self._ticker = ticker
        self._timeframe = timeframe
        self._stName = strategy['name']
        self._tp = round(strategy['tp'],2)
        self._sl = round(strategy['sl'],2)
        self.pi = Positioninfo(pair=self._ticker, size=1000)
        self.filePath = f'./TradesData/{self._stName}/P{self._period}-M{self._multiplier}/{self._timeframe}/{self._ticker}-{self._timeframe}-{self._stName}-{self._sl}-{self._tp}.csv'
        self._inposition = False
        self.simulating_res_df = pd.DataFrame()

    def open_position(self, row):
        
        self.pi.opendate = row['open_time']
        self.pi.openprice = row['close']
        self.pi.isclosed = False
        self.pi.executions = 'open'
        self.pi.qty = self.pi.size/self.pi.openprice
        self.pi.id = f'{self._ticker}-{(self.pi.opendate)}'
        self.pi.ptype = 'Buy' if row[self.trend_col] else 'Sell'
        # csvMgr.addNewPositionTocsv(self.pi,filePath=self.filePath)
        self.simulating_res_df = posMgr.add_position(
            self.pi, self.simulating_res_df)
        self._inposition = True

    def check_sl_tp(self, row):
        date_range_df = self.df_1m.loc[(self.df_1m['open_time'] >= row['open_time']) & (
            self.df_1m['close_time'] <= row['close_time'])]
        date_range_df = pd.DataFrame(date_range_df)
        hit = False
        info = {}
        if not hit:
            for index, minute_data in date_range_df.iterrows():
                if checktakeProfit(self.pi, date_range_df['high'][index], TPpercent=self._tp):
                    hit = True
                    info = {
                        'type': 'tp', 'price': date_range_df['high'][index], 'time': date_range_df['close_time'][index]}
                    break
                elif checkstoploss(self.pi, date_range_df['low'][index], slpercent=self._sl):
                    hit = True
                    info = {
                        'type': 'sl', 'price': date_range_df['low'][index], 'time': date_range_df['close_time'][index]}
                    break
        return hit, info

    def close_position(self, time, price, closetype):

        self.pi.closeprice = price
        self.pi.closedate = time
        self.pi.closetype = closetype
        self.pi.isAlive = False
        self.pi.isclosed = True
        self.pi.executions = closetype

        # csvMgr.positionEdit(self.pi,filePath=self.filePath)
        self.simulating_res_df = posMgr.edit_position(
            self.pi, self.simulating_res_df)
        self._inposition = False
        self.pi = Positioninfo(pair=self._ticker, size=1000)

    def check(self, row):
        index = row.name
        
        if index > self.data_df.index[0]:
      
            curr_trend = row[self.trend_col]
            prev_trend = self.data_df.loc[index-1,self.trend_col]

            if not self._inposition:

                if curr_trend != prev_trend:
                    self.open_position(row)
                    hit, info = self.check_sl_tp(row=row)

            else:
                if curr_trend == prev_trend:

                    hit, info = self.check_sl_tp(row=row)
                    if hit:
                        time = info['time']
                        price = info['price']
                        closetype = info['type']

                        self.close_position(time, price, closetype)

                else:
                    time = row['close_time']
                    price = row['close']
                    closetype = 'TC'
                    self.close_position(time, price, closetype)
                    self.open_position(row)

    def run_strategy(self):
        self.trend_col = f'ST-{float(self._period)}-{float(self._multiplier)}'
        # self.trend_col='isUpTrend'

        data_path = f'Data/{self._year}/{self._ticker}/{self._ticker}-{self._timeframe}.csv'
        m1_path =   f'Data/{self._year}/{self._ticker}/{self._ticker}-1m.csv'

        self.df_1m = pd.read_csv(m1_path)
        self.df_1m['open_time'] =  pd.to_datetime(self.df_1m['open_time'])
        self.df_1m['close_time'] = pd.to_datetime(self.df_1m['close_time'])

        self.data_df = pd.read_csv(data_path)
        self.data_df['open_time'] =  pd.to_datetime(self.data_df['open_time'])
        self.data_df['close_time'] = pd.to_datetime(self.data_df['close_time'])

        self.data_df = Supertrend(self.data_df, self._period, self._multiplier)
        self.data_df=self.data_df.loc[(self.data_df['open_time']>=self.start_date)&(self.data_df['close_time']<=self.end_date)]
        
        self.data_df.apply(self.check, axis=1)
        
        if self.save_to_db:
            csvMgr.check_dir_exist('TradesData',
             [ self._stName, f'P{self._period}-M{self._multiplier}', self._timeframe])

         
            self.simulating_res_df.to_csv(self.filePath, index=False)
            meta = {
                
                'st_config': 
                {
                    'ticker': self._ticker,
                    'timeframe': self._timeframe,
                    'period': self._period,
                    'multiplier': self._multiplier,
                    'tp': self._tp,
                    'sl': self._sl,
                    'year':self._year
                },
                'st_name': self._stName, 
                'path': self.filePath
                }

            csvMgr.AddMeta(meta)
        return self.simulating_res_df
