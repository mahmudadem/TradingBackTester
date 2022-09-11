from datetime import datetime
import time
import streamlit as st
import pandas as pd 
from _code.constants.constants import constants as cts
from _code.str_logic.ST_1_trend_logic import ST_1_strategy 
from _code.utils import CSVDataManager as csvMgr,results_calculator as calc




def set_State(key,val):
    if key not in st.session_state:
        st.session_state[key]=val
    else :
         st.session_state[key]=val   
    
def check_state(key,val):
    if key not in st.session_state:
        st.session_state[key]=val
    return st.session_state[key]
check_state('expander', True)
check_state('show_loading', False)
check_state('show_success', False)
check_state('show_results', False)
check_state('time_elapsed', 0)
check_state('results_df', pd.DataFrame())
check_state('override_old', False)
# st.session_state
st.subheader('SUPER TREND 1 TREND STRATEGY BACKTESTeR')



if not st.session_state.show_results:
    results=pd.DataFrame()

def run():
    check_state('period', period)
    del st.session_state.results_df


    strategy=ST_1_strategy(
        ticker=ticker,timeframe=timeframe,period=period,
        multiplier=multiplier,
        strategy=  {'name': 'ST1','tp': tp,'sl': sl },
        save=save_results,
        dates={'start_date':start_date,'end_date':end_date}
        )

    start_time=time.time()
    with st.spinner('Working on it ...'):
        results=strategy.run_strategy()

    set_State('results_df', results)

    end_time=time.time()
    set_State('time_elapsed',round(end_time-start_time,2))
    set_State('show_success',True)
    set_State('show_results',True)
    # st.session_state
    set_State('expander', False)
    




expander = st.expander("Strategy Configurations",expanded=st.session_state.expander)

col1, col2, col3,col4 = expander.columns(4)

with col1:
    ticker = st.selectbox(
     'Ticker',
     cts.pairs)
    start_date=st.date_input(label='start Date',key='start_date',value=datetime(year=2022,month=1,day=1))
    locally=st.checkbox(label='local datasets',value=True)
    save_results=st.checkbox(label='Save results',value=False)
with col2:
   
    period=st.number_input(label='period',value=10.0,step=0.1)
    end_date=st.date_input(label='End Date',key='end_date')
    posision_size =st.number_input(label='posision size $',value=1000,step=100)

with col3:
    multiplier=st.number_input(label='multiplier',value=10.0,step=0.1)
    tp=st.number_input(label='take profit',value=1.0,step=0.1)
    # st.text('posision_size')

with col4:
     timeframe = st.selectbox(
     'Time Frame',
     cts.timeFrames,index=1)
     sl=st.number_input(label='stop loss',value=1.0,step=0.1)
     


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
                st.session_state.show_results=True
                read_res_df=csvMgr.getTradesData(path) 
                st.session_state.show_results=True
                st.session_state.results_df=read_res_df

if st.session_state.show_loading:
        with st.spinner('Working on it ...'):
            set_State('show_loading',not st.session_state.show_loading)

if st.session_state.show_success:
    st.success(f'✅ Done! in: {st.session_state.time_elapsed} Seconds - {round(int(st.session_state.time_elapsed)/60,2)} Minutes ')
    set_State('show_success',not st.session_state.show_success)            


def get_analytics(df):
        analized_df=calc.calculate(df=df,metaData={'ticker':ticker,'timeframe':timeframe,'tp':tp,'sl':sl,'year':start_date.year})
        c=st.container()
        # c.text(f'TICKER={ticker} | TIMEFRAME= {timeframe} | PERIOD= {period} | MULTIPLEIR= {multiplier} ')

        # c.text(f'TP = {tp} | SL = {sl}')
        # c.dataframe(analized_df)
        col11,col22,col33,col44=c.columns(4)
        col11.text(f'TICKER={ticker}') 
        col11.text(f'TP = {tp}')
        col22.text(f'TIMEFRAME= {timeframe} ')
        col22.text(f'SL = {sl} ')

        col33.text(f'PERIOD= {period} ')

        col44.text(f'MULTIPLEIR= {multiplier} ')



        col1, col2, col3 = st.columns(3)
        col1.metric("All Positions", analized_df['positions_Count'], str(analized_df['total_profit/loss'].sum())+'$'+ ' =  ' +str(round(analized_df['total_profit/loss'].sum()/posision_size*100,2))+' %')
        col2.metric("Long", analized_df['long'][0]['c'], str(round(analized_df['long'][0]['s']/posision_size*100,2))+' %')
        col3.metric("Short",analized_df['short'][0]['c'], str(round(analized_df['short'][0]['s']/posision_size*100,2))+' %')
        headers=['Buy statictics','Sell statictics','Trend Change statictics']
        col_names=['long','short','TC']
        for i in range(3):
            df=pd.DataFrame(columns=['Count','Take Profit','Stop Loss','Trend Change','Total profit/loss'],
            data=[[analized_df[col_names[i]][0]['c'],analized_df['win_'+col_names[i]][0][0],analized_df['win_'+col_names[i]][0][1],analized_df['win_'+col_names[i]][0][2],analized_df[col_names[i]][0]['s']]]
            )
            df['Total profit/loss %']=df['Total profit/loss']*100/posision_size
            st.subheader(headers[i])
            st.table(df)
       
        return c
# results
if st.session_state.show_results:
    results=st.session_state.results_df
    # l=f'RESULTS: Symbol={ticker} ------- TimeFrame={timeframe} ------- P/M={period}/{multiplier} ------- TP/SL={tp}/{sl}'
    data_ex=st.expander(label='RESULTS  ',expanded=True)
    
    analytics, chart,data = data_ex.tabs(["📊 Analytics","📈 Charts","🗃 Datasets"])
    

    analytics.subheader("Simulating analytics")
    with analytics:
        get_analytics(df=results)

    chart.subheader("Profit/Loss Chart")
    chart.selectbox(label='Metric',options=['AccPL','closetype'])
    chart.line_chart(results[['opendate','AccPL']],x='opendate',use_container_width=True)

    data.subheader("Data Frame")
    data.dataframe(results)