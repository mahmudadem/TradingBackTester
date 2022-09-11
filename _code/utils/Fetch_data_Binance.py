
import pandas as pd
import datetime
from super_indicator import calculate
from binance.client import Client
import CSVDataManager as csvMGr
from constants import constants as cts


apiPub = 'S6NF8GDIOmhvWyx44rpsSYMfOL9niCE3SLXKU87R5Tq5Xg4aHTYrmjCquBZ4KuNY'
api_sec = 'xO4bupdK7ddNIJAg121yV5tR1yxRKpAqwTK9MAZQb5tCeifxMxbqxKNKtxbsv6L2'
client = Client(apiPub, api_sec)
interval = {'1m': Client.KLINE_INTERVAL_1MINUTE,
            '5m': Client.KLINE_INTERVAL_5MINUTE,
             '15m': Client.KLINE_INTERVAL_15MINUTE,
              '30m': Client.KLINE_INTERVAL_30MINUTE,
              '1hour': Client.KLINE_INTERVAL_1HOUR,
              '4hour': Client.KLINE_INTERVAL_4HOUR,
              '1day': Client.KLINE_INTERVAL_1DAY,
              '1month': Client.KLINE_INTERVAL_1MONTH, }


def get_ticker_data(ticker, time_frames, time_range):

    for time_frame in time_frames:
        data = client.get_historical_klines(
        ticker, interval[time_frame], time_range['start'], time_range['end'])
        df = pd.DataFrame(data)
        df.columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'Quote asset volume',
                      'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
        df2 = df.drop(df.columns[[7, 8, 9, 10, 11]], axis=1)
        df2['open_time'] = pd.to_datetime(df2['open_time'], unit='ms')
        df2['close_time'] = pd.to_datetime(df2['close_time'], unit='ms')
        df2['open'] = round(df2['open'].astype(float), 5)
        df2['high'] = round(df2['high'].astype(float), 5)
        df2['low'] = round(df2['low'].astype(float), 5)
        df2['close'] = round(df2['close'].astype(float), 5)
        df2['volume'] = round(df2['volume'].astype(float), 5)


        if time_frame!='1m' :
                df2 = calculate(df2, 20, 10)
                df2['BLB'] = round(df2['BLB'].astype(float), 5)
                df2['BUB'] = round(df2['BLB'].astype(float), 5)
                df2 = df2[['open_time', 'open', 'high', 'low', 'close',
                        'close_time', 'volume', 'BLB', 'BUB', 'isUpTrend']]
        else :
            df2 = df2[['open_time', 'open', 'high', 'low', 'close',
                    'close_time']]    
        # date=datetime.strptime(asd,'%d %b,%Y')
        year=datetime.datetime.strptime(time_range['start'],'%d %b,%Y').year            
        df2.to_csv(f'data/{year}/{ticker}/{ticker}-{time_frame}.csv', index=False)

base_dir='Data'
years=['2022']
# timeframes=['1m','5m','15m','30m','1hour','4hour','12hour','1day']
timeframes=['1hour']
tickers=cts.pairs
for year in years:
        for timeframe in timeframes:
                for ticker in tickers:
                        csvMGr.check_dir_exist(ParentPath=base_dir,subPaths=[year,ticker.upper()])
                        path=f'{base_dir}/{year}/{ticker.upper()}'
                        filepath=f'{path}/{ticker.upper()}-{timeframe}.csv'
                        
                        get_ticker_data(ticker.upper(),[timeframe],{'start':'1 Jan,2022','end':'31 Aug,2022'})

