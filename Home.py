import streamlit as st
import pandas as pd 
import numpy as np

st.title("Welcome to Trading Bot Backtesting Tool")

st.header('you can choose what to do from side bar')

# st.text(hl.hello())
import os
os.environ['API_KEY'] = 'a0j6239f_Tu6tSaLmsc8t7RoaWh343FW6aTBc1f9Z'

st.write(os.getenv('API_KEY'))