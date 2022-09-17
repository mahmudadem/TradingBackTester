from datetime import datetime
import time
import streamlit as st
import pandas as pd 
from _code.constants.constants import constants as cts
from _code.str_logic.ST_1_trend_logic import ST_1_strategy 
from _code.utils.common_utils import Notifier
from _code.utils import CSVDataManager as csvMgr,results_calculator as calc
from _code.utils.Auth import UserAuth 

st.set_page_config(
     page_title="SuperTrend Strategy Back Testing",
     page_icon="📈",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://www.google.com/",
         'About': "# Trading Back Test tool Made by\n Mahmud Adem \n mahmudadem90@gmail.com"
     }
 )

page_content=st.empty()

def set_State(key,default):
    if key not in st.session_state:
        st.session_state[key]=default
    else :
         st.session_state[key]=default   
    
def check_state(key,default):
    if key not in st.session_state:
        st.session_state[key]=default
    return st.session_state[key]

def config_changed():
    st.session_state.show_results=False
    st.session_state.expander=True

def current_values():
    return{
        'year':check_state('dates','>> dates in not in state')[0].year,
        'ticker':check_state('ticker','>> no not  found in state'),
        'locally':check_state('locally','>> locally not found in state'),
        'save_results':check_state('save_results','>> save_results ticker found in state'),
        'timeframe':check_state('timeframe','>> timeframe not found in state'),
        'tp':float(check_state('tp','>> tp not found in state')),
        'sl':float(check_state('sl','>> sl not found in state')),
        'start_date':check_state('start_date','>> start date not found in state'),
        'end_date':check_state('end_date','>> end_date not found in state'),
        'period':float(check_state('period','>> period  not found in state')),
        'multiplier':float(check_state('multiplier','>> multiplier  not found in state')),
        'position_size':float(check_state('position_size','>> posision_size  not found in state')),
        'dates':check_state('dates','>> dates  not found in state'),
    }
def get_analytics(df):
        values=current_values()
        analized_df=calc.calculate(df=df,
        metaData=
                    {'ticker':values['ticker']
                    ,'timeframe':values['timeframe']
                    ,'tp':values['tp']
                    ,'sl':values['sl']
                    ,'year':values['start_date'].year
                    })
        c=st.container()
        col11,col22,col33,col44=c.columns(4)
        col11.caption('TICKER= {}'.format(values['ticker'])) 
        col11.caption('TP = {} %'.format(values['tp']))
        col22.caption('TIMEFRAME= {} '.format(values['timeframe']))
        col22.caption('SL = {} %'.format(values['sl']))

        col33.caption('PERIOD= {} '.format(values['period']))
        col33.caption('Start: {} '.format(values['start_date']))

        col44.caption('MULTIPLEIR= {} '.format(values['multiplier']))
        col44.caption('End: {} '.format(values['end_date']))


        position_size=values['position_size']
        col1, col2, col3 = st.columns(3)
        col1.metric("All Positions", analized_df['positions_Count'], str(analized_df['total_profit/loss'].sum())+'$'+ ' =  ' +str(round(analized_df['total_profit/loss'].sum()/position_size*100,2))+' %')
        col2.metric("Long Positions", analized_df['long'][0]['c'], str(round(analized_df['long'][0]['s']/position_size*100,2))+' %')
        col3.metric("Short Positions",analized_df['short'][0]['c'], str(round(analized_df['short'][0]['s']/position_size*100,2))+' %')
        headers=['Buy statictics','Sell statictics','Trend Change statictics']
        col_names=['long','short','TC']
        for i in range(3):
            df=pd.DataFrame(columns=['Count','Take Profit','Stop Loss','Trend Change','Total profit/loss'],
            data=[[analized_df[col_names[i]][0]['c'],analized_df['win_'+col_names[i]][0][0],analized_df['win_'+col_names[i]][0][1],analized_df['win_'+col_names[i]][0][2],analized_df[col_names[i]][0]['s']]]
            )
            df['Total profit/loss %']=df['Total profit/loss']*100/position_size
            st.subheader(headers[i])
            st.table(df)
       
        return c


@st.cache
def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
def run():

    values=current_values()
    check_state('period', values['period'])
    del st.session_state.results_df
    strategy=ST_1_strategy(
        ticker=values['ticker'],timeframe=values['timeframe'],period=values['period'],
        multiplier=values['multiplier'],
        strategy=  {'name': 'ST1','tp': values['tp'],'sl': values['sl'] },
        save=values['save_results'],
        dates={'start_date':values['start_date'],'end_date':values['end_date']}
        )
    start_time=time.time()
    with page_content:
        with st.spinner('Working on it ...'):
            
            results=strategy.run_strategy(locally=values['locally'])
            Notifier().done()
    set_State('results_df', results)

    end_time=time.time()
    set_State('time_elapsed',round(end_time-start_time,2))
    set_State('show_success',True)
    set_State('show_results',True)
    # st.session_state
    set_State('expander', False)
    
def get_available_dates(year=2022,timeframe='5m'):
    year=check_state('dates',0)[0].year
    ticker=check_state('ticker','no ticker found in state')
    timeframe=check_state('timeframe','timeframe not found in state')
    path=f'./Data/{year}/{ticker}/{ticker}-{timeframe}.csv'
    df=pd.read_csv(path,parse_dates=['open_time'])
    begining=df.head(1)['open_time'].dt.date.values[0]
    end=df.tail(1)['open_time'].dt.date.values[0]
    return [begining,end]


def get_test_meta():
    if not check_state('save_results',False):
        return (None,datetime.now().strftime("%d-%m-%Y %H:%M "))
    
    values=current_values()
    year=values['dates'][0].year
    ticker=values['ticker']
    timeframe=values['timeframe']
    tp=float(values['tp'])
    sl=float(values['sl'])
    period=float(values['period'])
    multiplier=float(values['multiplier'])
    path=f'./TradesData/MetaData.csv'
    test_id=f'{year}-{ticker.upper()}-{timeframe}-{period}-{multiplier}-{sl}-{tp}'
    df=pd.read_csv(path)
    id_=df.loc[df['id']==test_id]['id']
    execution_Date=df.loc[df['id']==test_id]['execution_date'].head().values
    return (id_,str(execution_Date[0]))

def authrized_content():
    check_state('expander', True)
    check_state('show_loading', False)
    check_state('show_success', False)
    check_state('show_results', False)
    check_state('time_elapsed', 0)
    check_state('results_df', pd.DataFrame())
    check_state('override_old', False)
    check_state('dates', [datetime(year=2022,month=1,day=1),None])

    st.subheader('SUPER TREND 1 TREND STRATEGY BACKTeSTeR')
    expander = st.expander("Strategy Configurations",expanded=st.session_state.expander)

    col1, col2, col3,col4 = expander.columns(4)

    with col1:
        ticker = st.selectbox(
        'Ticker',
        cts.pairs,key='ticker')
        start_date=st.date_input(label='Start Date',key='start_date',value=st.session_state.dates[0],on_change=config_changed)
        locally=st.checkbox(label='Local Datasets',key='locally',value=True,disabled=True,help='If enabled Test will run on locally saved datasets, most recent candles data may not be included, \n otherwise you need to provide Exchange API credintials in order to get recent candles data from there API  ')
        save_results=st.checkbox(label='Save Results',key='save_results',value=False)

       
    with col2:
    
        period=st.number_input(label='Period',key='period',value=10.0,step=0.1,on_change=config_changed)
        end_date=st.date_input(label='End Date',key='end_date',value=st.session_state.dates[1],on_change=config_changed)
        posision_size =st.number_input(label='Position Size $',key='position_size',value=1000,step=100,on_change=config_changed)

    
    with col3:
        multiplier=st.number_input(label='Multiplier',key='multiplier',value=10.0,step=0.1,on_change=config_changed)
        tp=st.number_input(label='Take Profit',key='tp',value=1.0,step=0.1,on_change=config_changed)
        # st.text('posision_size')

    with col4:
        timeframe = st.selectbox('Time Frame',key='timeframe',options=cts.timeFrames,index=1,on_change=config_changed)
        sl=st.number_input(label='Stop Loss',key='sl',value=1.0,step=0.1,on_change=config_changed)
        
    set_State('dates', get_available_dates(start_date.year))


    plh=st.empty()
    plh.button(label='Start Simulating ⚡',on_click=run,key='start_btn1',disabled=False)
    if save_results:
        
        path=f'TradesData/ST1/P{period}-M{multiplier}/{timeframe}/{ticker}-{timeframe}-ST1-{sl}-{tp}.csv'
        if csvMgr.check_file_exist(path) :
                container=plh.container()
                container.error("⚠️ A simulating File with same config found, continue will override old data")
                if container.button("Ignore old Data and continue"):
                    plh.button(label='Start Simulating ⚡',on_click=run,key='start_btn3',disabled=False)
                
                else :
                    read_res_df=csvMgr.getTradesData(path) 
                    st.session_state.show_results=True
                    st.session_state.results_df=read_res_df

    if st.session_state.show_loading:
            with st.spinner('Working on it ...'):
                set_State('show_loading',not st.session_state.show_loading)

    if st.session_state.show_success:
        st.success(f'✅ Done in: {st.session_state.time_elapsed} Seconds = {round(int(st.session_state.time_elapsed)/60,2)} Minutes ')
        set_State('show_success',not st.session_state.show_success)            


    if st.session_state.show_results:
        results=st.session_state.results_df
        data_ex=st.expander(label=f'RESULTS  ',expanded=True)
        
        analytics, chart,data = data_ex.tabs(["📊 Analytics","📈 Charts","🗃 Datasets"])
        

        analytics.markdown("##### `Execution date`   : "+f' {get_test_meta()[1]}   ')
        with analytics:
            get_analytics(df=results)

        chart.subheader("Profit/Loss Chart")
        chart.selectbox(label='Metric',options=['AccPL','closetype'])
        chart.line_chart(results[['opendate','AccPL']],x='opendate',use_container_width=True)

        data_col1,space,data_col2=data.columns(3)

        data_col1.subheader("Simulating Results Data")
        

        csv = convert_df(results)

        data_col2.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=f'{ticker}-{timeframe}-{start_date}-{end_date}.csv',
        mime='text/csv',
        )
        data.dataframe(results)



if 'auth_object' not in st.session_state: 
    user_auth= UserAuth()
else :
    user_auth=st.session_state['auth_object']




with st.spinner('Loading....'):
    user_auth.get_cook()
    
    if user_auth.user_authenticated and st.session_state.authentication_status:
        with page_content:
            with st.container():
                authrized_content()
            user_auth.logout()    
    else:
        user_auth.authenticate_user()            