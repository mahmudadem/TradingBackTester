from datetime import datetime
from queue import Empty
import time
import streamlit as st
import pandas as pd 
import numpy as np
from _code.constants.constants import constants as cts
from _code.str_logic.ST_1_trend_logic import ST_1_strategy 




st.error("Do you really, really, wanna do this?")
if st.button("Yes I'm ready to rumble"):
    st.text('asd')


import streamlit as st
import time


placeholder = st.empty()
btn = placeholder.button('Button', disabled=False, key='1')


if btn:
    co=placeholder.container()
    time.sleep(1)
    co.text('asd')
    b=co.button('aa')
    time.sleep(1)
    if b : placeholder.button('Button2', disabled=True, key='2')