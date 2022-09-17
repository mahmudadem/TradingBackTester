
class messeges:
  guest='''#
  In **Guest mode** you will be able to run test of your choice, but not to save your
  favourit settings and tests configurations, it's better to **signup/login**  with your account for that matter.
  
  '''
class constants:

    TradesfileColumns = ['number','type','qty','size', 'opendate','openprice','closeprice','closedate','isclosed','closetype','p/l','AccPL','executions','id']
    MetaFileColumns = ['number','id','execution_date','strategy_name','strategy_config', 'result_path']

    timeFrames=['1m','5m','15m','30m','1hour','4hour']

    pairs=[
    'XTZUSDT', 'ETHUSDT', 'SOLUSDT', 'LINKUSDT', 'DOTUSDT', 'XRPUSDT', 'THETAUSDT',
     'AAVEUSDT', 'BNBUSDT', 'LTCUSDT', 'ADAUSDT', 'UNIUSDT', 'EOSUSDT', 'BTCUSDT',
      'AVAXUSDT', 'CHZUSDT', 'FTMUSDT', 'TRXUSDT', 'MANAUSDT', 'ZECUSDT', 'XLMUSDT', 
      'BCHUSDT', 'LUNAUSDT', 'ICPUSDT', 'SANDUSDT', 'ALICEUSDT'
    ]
    db_base_dir='./TradesData'

    price_scales={'BTCUSD': '2', 'ETHUSD': '2', 'EOSUSD': '3', 'XRPUSD': '4', 'DOTUSD': '3', 'BITUSD': '3', 'BTCUSDT': '2', 'ETHUSDT': '2', 'EOSUSDT': '3', 'XRPUSDT': '4', 'BCHUSDT': '2', 'LTCUSDT': '2', 'XTZUSDT': '3', 'LINKUSDT': '3', 'ADAUSDT': '4', 'DOTUSDT': '3', 'UNIUSDT': '3', 'XEMUSDT': '4', 'SUSHIUSDT': '3', 'AAVEUSDT': '2', 'DOGEUSDT': '4', 'MATICUSDT': '4', 'ETCUSDT': '3', 'BNBUSDT': '2', 'FILUSDT': '2', 'SOLUSDT': '3', 'XLMUSDT': '5', 'TRXUSDT': '5', 'VETUSDT': '5', 'THETAUSDT': '3', 'COMPUSDT': 
'2', 'AXSUSDT': '3', 'LUNAUSDT': '3', 'SANDUSDT': '4', 'MANAUSDT': '4', 'KSMUSDT': '2', 'ATOMUSDT': '3', 'AVAXUSDT': '3', 'CHZUSDT': '5', 'CRVUSDT': '3', 'ENJUSDT': '4', 'GRTUSDT': '4', 'SHIB1000USDT': '6', 'YFIUSDT': '0', 'BSVUSDT': '2', 'ICPUSDT': '2', 'FTMUSDT': '4', 'ALGOUSDT': '4', 'DYDXUSDT': '3', 'NEARUSDT': '3', 'SRMUSDT': '3', 'OMGUSDT': '3', 'IOSTUSDT': '5', 'DASHUSDT': '2', 'FTTUSDT': '2', 'BITUSDT': '3', 'GALAUSDT': '5', 'CELRUSDT': '5', 'HBARUSDT': '5', 'ONEUSDT': '5', 'C98USDT': '4', 'COTIUSDT': '4', 'ALICEUSDT': '3', 'EGLDUSDT': '2', 'RENUSDT': '4', 'KEEPUSDT': '4', 'TLMUSDT': '4', 'RUNEUSDT': '3', 'ILVUSDT': '1', 'FLOWUSDT': '2', 'WOOUSDT': '4', 'LRCUSDT': '4', 'ENSUSDT': '2', 'IOTXUSDT': '5', 'CHRUSDT': '4', 'BATUSDT': '4', 'STORJUSDT': '4', 'SNXUSDT': '3', 'SLPUSDT': '5', 'ANKRUSDT': '5', 'LPTUSDT': '2', 'QTUMUSDT': '3', 'CROUSDT': '5', 'SXPUSDT': '4', 'YGGUSDT': '3', 'ZECUSDT': '2', 'IMXUSDT': '3', 'SFPUSDT': '4', 'AUDIOUSDT': '4', 'ZENUSDT': '2', 'SKLUSDT': 
'5', 'BTTUSDT': '6', 'GTCUSDT': '3', 'LITUSDT': '3', 'CVCUSDT': '4', 'RNDRUSDT': '3', 'SCUSDT': '5', 'RSRUSDT': '5', 'STXUSDT': '3', 'MASKUSDT': '3', 'CTKUSDT': '3', 'BICOUSDT': '3', 'REQUSDT': '4', '1INCHUSDT': '4', 'KLAYUSDT': '4', 'SPELLUSDT': '5', 'ANTUSDT': '3', 'DUSKUSDT': '4', 'ARUSDT': '2', 'REEFUSDT': '6', 'XMRUSDT': '2', 'PEOPLEUSDT': '5', 'IOTAUSDT': '4', 'CELOUSDT': '3', 'WAVESUSDT': '3', 'RVNUSDT': '5', 'KNCUSDT': '4', 'KAVAUSDT': '3', 'ROSEUSDT': '4', 'DENTUSDT': '6', 'CREAMUSDT': '2', 'BTCUSDM22': '2', 'BTCUSDH22': '2', 'ETHUSDM22': '2', 'ETHUSDH22': '2'}
