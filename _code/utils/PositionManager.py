import csv
from os import error
from datetime import datetime
import time
import pandas as pd
from pathlib import Path
from ..models.Positioninfo import  Positioninfo
from ..constants.constants import  constants as cts
import warnings

warnings.filterwarnings('ignore')



def createNewTradingFile(filePath):   
        path=f'{filePath}.csv' if '.csv' not in filePath else filePath     

        with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=cts.csvcolumns)
                writer.writeheader()
        
def check_file_exist(filePath,createIfNot=False):

        path=f'{filePath}.csv' if '.csv' not in filePath else filePath     
        my_file = Path(path)
        if not my_file.is_file() and createIfNot:
                createNewTradingFile(filePath)   
        return  my_file.is_file()
 


def check_dir_exist(ParentPath,subPaths):
        
        if not Path(ParentPath).is_dir():
               Path(ParentPath).mkdir() 

        if Path(ParentPath).is_dir():
         for dir in subPaths:
           ParentPath+='/'+dir     
           sub_path= Path(dir)  
           if not Path(ParentPath).is_dir() :
                my_path=Path(ParentPath)
                my_path.mkdir()            

def dataFortmater(positionData:Positioninfo):
        formatedData={
        'number':positionData.number,
        'id':positionData.id,
        'type':positionData.ptype,
        'size':positionData.size,
        'opendate':positionData.opendate,
        'openprice':positionData.openprice,
        'closeprice':positionData.closeprice,
        'closedate':positionData.closedate,
        'isclosed':positionData.isclosed,
        'closetype':positionData.closetype,
        'p/l':0.0,
        'AccPL':0.0,
        'qty':round(positionData.qty,3),
        'executions':positionData.executions,
        }

        return formatedData

def add_position(pdata:Positioninfo,df :pd.DataFrame):
        last_trad_number=df['number'].iloc[-1] if len(df) >0 else 0
        
        pdata.number=int(last_trad_number)+1
        df=df.append(dataFortmater(pdata),ignore_index=True)        
        return df

def edit_position(pdata:Positioninfo,df:pd.DataFrame,include_comission=True):
     try:  
       
       
       
        index=df[df['id']==pdata.id].index.values.astype(int)[0]
        # if 'on_trend_multiple' in str(filePath) :
        #         datafromcsv['qty'][index]=round(pdata.qty,3)
        #         datafromcsv['size'][index]=pdata.size
        #         datafromcsv['openprice'][index]=round(pdata.openprice,4)

        df['executions'][index]=str(df['executions'][index])+'->'+str(pdata.executions)
        df['closeprice'][index]=pdata.closeprice
        df['closetype'][index]=pdata.closetype
        df['closedate'][index]=pdata.closedate
        df['isclosed'][index]=pdata.isclosed

        if pdata.isclosed:
                commission=0
                if include_comission:
                    commission=(float(pdata.size)*0.0015)
                if pdata.ptype=='Buy':
                        pro_loss=((float(pdata.closeprice)-float(pdata.openprice))*float(pdata.qty))-commission
                        df['p/l'][index]=round(pro_loss,2)
                        df['AccPL'][index]=round(df['p/l'].sum(),2)
                else:
                        pro_loss=((float(pdata.openprice)-float(pdata.closeprice))*float(pdata.qty))-commission
                        df['p/l'][index]=round(pro_loss,2)
                        df['AccPL'][index]=round(df['p/l'].sum(),2)
        return df
        
     except Exception as e :
               log=f'SOME THING WENT WRONG WHILE TRYING TO EDIT POSITONS IN  \
                : \n {str(e)}--{pdata.closeprice}-{pdata.openprice}-size={pdata.size}-qty={pdata.qty}'
               print(pdata.pair.upper(),log)



# write_events_Log("aliceusdt",'5m','test')
# tempdata=Positioninfo()
# tempdata.pair="avaxusdt"
# tempdata.id='2c965550-b90b-4f32-b13d-f868e72734d0'
# tempdata.isclosed=True
# tempdata.closeprice=92.5
# # tempdata.qty=''
# tempdata.openprice=91.78
# tempdata.closetype='tc'
# tempdata.closedate='2022-01-11T10:25:22Z'
# tempdata.executions='tc'
# positionEdit(tempdata,'5m')
# addNewPositionTocsv(pdata=tempdata,timeframe='5m')
# print(get_last_Pos_PL(tempdata,'1m'))
# tempdata.size=1000
# tempdata.ptype=cts.Long
# tempdata.openprice=60000
# tempdata.opendate="27/10/2021"
# tempdata.ptype=cts.long
# addNewPositionTocsv(tempdata,cts.one_mimute)

# print(checkNoPosition(tempdata,cts.one_mimute))

# tempdata=Positioninfo()
# tempdata.pair="aaveusdt"
# tempdata.closedate="2021/10/27"
# tempdata.closeprice=183.8
# tempdata.closetype=cts.trendchange
# positionEdit(tempdata,cts.one_mimute)


# for i in cts.pairs:
#          createNewTradingFile(pair=i,timeframe='1m')

