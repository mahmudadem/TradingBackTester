from codecs import ignore_errors
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


def createNewTradingFile(filePath,filetype):   
        path=f'{filePath}.csv' if '.csv' not in filePath else filePath     

        with open(path, 'w', encoding='UTF8', newline='') as f:
                writer = csv.DictWriter(f,
                 fieldnames=cts.TradesfileColumns if filetype=="T" else cts.MetaFileColumns)
                writer.writeheader()
        
def check_file_exist(filePath,createIfNot=False,filetype="T"):

        path=f'./{filePath}.csv' if '.csv' not in filePath else f'./{filePath}'     
        my_file = Path(path)
        if not my_file.is_file() and createIfNot:
                createNewTradingFile(filePath,filetype=filetype)   
        return  my_file.is_file()
 
def AddMeta(meta):
        st_name=meta['st_name']
        st_config=meta['st_config']
        result_path=meta['path']
        exe_date=datetime.strftime(datetime.now(),"%d-%m-%Y %H:%M")
        id=f'{st_config["year"]}-{st_config["ticker"]}-{st_config["timeframe"]}-{int(st_config["period"])}-{int(st_config["multiplier"])}-{int(st_config["sl"])}-{int(st_config["tp"])}'
        meta_file_path=f'{cts.db_base_dir}/MetaData.csv'
        check_file_exist(meta_file_path,createIfNot=True,filetype="M")
        Meta_df=pd.read_csv(meta_file_path)
        row_exist=Meta_df.loc[(Meta_df['id']==id)]
        if  row_exist.empty:
                number=Meta_df['number'].iloc[-1]+1 if len(Meta_df)>0 else 0
                data={
                        'number':number
                        ,'id':id
                        ,'execution_date':exe_date
                        ,'strategy_name':st_name
                        ,'strategy_config':st_config
                        ,'result_path':result_path
                }
                Meta_df=Meta_df.append(data,ignore_index=True)
        else:   
                Meta_df.loc[row_exist.number.values[0],['execution_date']]=exe_date       
        Meta_df.to_csv(meta_file_path,index=False)

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

def addNewPositionTocsv(pdata:Positioninfo,filePath):
        filename=f'{filePath}.csv'
        datafromcsv=pd.read_csv(filename)
        lasttradnumber=datafromcsv['number'].iloc[-1] if len(datafromcsv) >0 else 0
        
        pdata.number=int(lasttradnumber)+1
        with open(filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=cts.csvcolumns)
            writer.writerow(dataFortmater(pdata))

def positionEdit(pdata:Positioninfo,filePath):
     try:  
        filename=f'{filePath}.csv'
       
        datafromcsv=pd.read_csv(filename)
        index=datafromcsv[datafromcsv['id']==pdata.id].index.values.astype(int)[0]
        if 'on_trend_multiple' in str(filePath) :
                datafromcsv['qty'][index]=round(pdata.qty,3)
                datafromcsv['size'][index]=pdata.size
                datafromcsv['openprice'][index]=round(pdata.openprice,4)

        datafromcsv['executions'][index]=str(datafromcsv['executions'][index])+'->'+str(pdata.executions)
        datafromcsv['closeprice'][index]=pdata.closeprice
        datafromcsv['closetype'][index]=pdata.closetype
        datafromcsv['closedate'][index]=pdata.closedate
        datafromcsv['isclosed'][index]=pdata.isclosed

        if pdata.isclosed:
                if pdata.ptype=='Buy':
                        pro_loss=((float(pdata.closeprice)-float(pdata.openprice))*float(pdata.qty))-(float(pdata.size)*0.0015)
                        datafromcsv['p/l'][index]=round(pro_loss,2)
                        datafromcsv['AccPL'][index]=round(datafromcsv['p/l'].sum(),2)
                else:
                        pro_loss=((float(pdata.openprice)-float(pdata.closeprice))*float(pdata.qty))-(float(pdata.size)*0.0015)
                        datafromcsv['p/l'][index]=round(pro_loss,2)
                        datafromcsv['AccPL'][index]=round(datafromcsv['p/l'].sum(),2)
        
        datafromcsv.to_csv(filename, index=False)
        
     except Exception as e :
               log=f'SOME THING WENT WRONG WHILE TRYING TO EDIT POSITONS IN CSV FILE : \n {str(e)}--{pdata.closeprice}-{pdata.openprice}-size={pdata.size}-qty={pdata.qty}'
               print(pdata.pair.upper(),log)
        #        write_events_Log(pdata.pair,timeframe,log,filePath)
               datafromcsv.to_csv(filename, index=False)

def halve_position(pdata:Positioninfo,timeframe):
       

        inposition,current_pos=check_open_Position(pdata,timeframe)
        if inposition:
                pdata.size=current_pos.size/2
                positionEdit(pdata,timeframe)
                current_pos.size=current_pos.size/2
                addNewPositionTocsv(current_pos,timeframe,ishalving=True)
                return(True,current_pos) 

def getTradesData(file_path=''):
        path=f'./{file_path}.csv' if '.csv' not in file_path else f'./{file_path}'
        try:
                # filepath=f'{folder_path}/{timeframe}/{pair}-{timeframe}.csv'
                datafromcsv=pd.read_csv(file_path)
                return datafromcsv
        except error as Exception:
                print(error)

def check_open_Position(pair,timeframe='5m',folder_path='Not Set'):
        df=getTradesData(pair,timeframe=timeframe,folder_path=folder_path)
        inPosition=False
        opened_pdata=None
        for i in range(0,len(df.index)):
            isClosed=df['isclosed'][i]
            
            if isClosed :
                pass
            else :
              if i==(len(df.index)-1):
                #   print("there is an opened position and it is the last position for this pair")            
                #   inPosition=True
                #   opened_pdata=get_position_info(df,i)
                pass
              else:
                #   inPosition=True
                  print(pair.upper()," from csvmanger check: found unclosed position and its not the last position for this pair:")           
        last_pos_data=get_position_info(df,len(df)-1)
        last_pos_data.pair=pair
        if last_pos_data.isclosed:
                inPosition=False
        else:
                inPosition=True        
        return (inPosition,last_pos_data)     

def  get_position_info(df,index):
            pi=Positioninfo()
        #     i=len(df.index)-1
            pi.isclosed=df['isclosed'][index]
        #     pi.pair=df['pair'][index]
            
            pi.ptype=df['type'][index]
            pi.size=df['size'][index]
            pi.opendate=df['opendate'][index]
            pi.openprice=df['openprice'][index]
        #     pi.executions=df['executions'][index]
            pi.id=df['id'][index]
            pi.qty=df['qty'][index]
            
            return pi

def get_last_Pos_PL(pdata:Positioninfo,timeframe):
        df=getTradesData(pdata,timeframe)
        i=len(df.index)-1
        if df['isclosed'][i]:
           pl=df['p/l'][i]
        else:
           pl=df['p/l'][i-1]        
        return pl

def write_events_Log(pair,timeframe,log,path='Not Set'):
        now=datetime.utcnow()
        # check_dir_exist('events-logs',timeframe)
        full_path=f"./events-logs/{path}/{timeframe}/{pair.upper()}-{timeframe}-Events_LOG.txt"
        
        f = open(full_path, "a")
        _log=f'\n{str(now.strftime("%c"))} -- {log}'
        f.write(_log)
        f.close() 

def add_execution(pair,pos_id,message,trigger,timeframe='5m',folder_path='Not set'):
        filename =f'{folder_path}/{timeframe}/1-executions-{timeframe}.csv'
       
        with open(filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['pair','trigger','pos_id','message'])
            row={'pair':pair,'pos_id':pos_id,'message':message,'trigger':trigger}
            writer.writerow(row)





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

