import time
import streamlit as st
from _code.utils.Auth import UserAuth

st.session_state
def authrized_content():
    st.write('You authrized') 
c,c1,c2= st.columns(3)
with c1:
    with st.spinner('middle loading'):
        time.sleep(0.5)
        # st.text_area('')

page_content=st.empty()

if 'auth_object' not in st.session_state: 
    user_auth= UserAuth()
else :
    user_auth=st.session_state['auth_object']

user_auth.get_cook()
with st.spinner('Loading....'):
    
    time.sleep(0.1)
    st.text('')
    if user_auth.user_authenticated and st.session_state.authentication_status:
        with page_content:
                    
                    with st.container():
                        authrized_content()
                    user_auth.logout()   
    else:   
        user_auth.authenticate_user()                    
st.session_state        