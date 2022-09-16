from datetime import datetime
from queue import Empty
import time
import streamlit as st
import pandas as pd 
import numpy as np
from _code.constants.constants import constants as cts
from _code.str_logic.ST_1_trend_logic import ST_1_strategy 


st.set_page_config(
     page_title="Live Trading -TEST-",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.google.com',
         'Report a bug': "https://www.google.com",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

st.header('TEST Live Trading') 

