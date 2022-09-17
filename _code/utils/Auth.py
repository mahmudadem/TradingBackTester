from datetime import datetime
import streamlit as st 
import re
import streamlit_authenticator as  stAuth
import streamlit_option_menu as op_menu
from _code.utils.Deta_db import user_db
from _code.utils.exceptions import *
from _code.constants.constants import messeges

class UserAuth:
    def __init__(self,callBack=None) -> None:
        self.callBack=callBack
        st.session_state['auth_object']=self
        self.db_ref=user_db('users')
        __all_users=self.db_ref.fetch({})
        self.cookie_name='cookmook'
        self.users_dic={'usernames':
            {
                 user_info['user_name']:
                                    {
                                       'name': user_info['name'],
                                        'password':user_info['password'],
                                        'email':user_info['email'],
                                        'user_key':user_info['key'],
                                    }for user_info in __all_users.items
            } }
        self.user_authenticated=False
        self.get_cook()
    def authenticate_user(self):
        # self.authenticator = stAuth.Authenticate(credentials=self.users_dic,cookie_name='cookmook',key='any',cookie_expiry_days=30,preauthorized=[''])
        if not self.user_authenticated  :
                menu=op_menu.option_menu('Welcome Back' ,options=['Log in','sign up','Guest Mode'],orientation='horizontal',
                    icons=['bi-person-fill','bi-person-plus-fill'],
                menu_icon='bi-graph-up-arrow',key='h_menu',
                
            )
                if menu=='Log in':
                    self.login()
                    
                elif menu=='sign up':
                    self.signup() 
                else :
                    st.header('Geust Mode ')
                    st.markdown(messeges().guest)       
        else :
            # self.logout()
            pass
    
    def check_available(self,field,value):
        data=self.db_ref.fetch(query={field:value})
        data
        if data.count > 0:
            return False
        else:   
            return  True   

    def validate(self,values):
        for entry in values:
            if entry=='user_name':
                if not self.check_available('user_name',values[entry]):
                    st.error('User name already exist')
                    return False
            elif entry=='passwords':
                if values[entry][0] != values[entry][1]:
                    st.error('Passwords do not match!')
                    return False
                elif len(values[entry][0]) < 5:
                    st.error('Passwords Must contail at least 5 charachters')
                    return False
            elif entry=='email':
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if not (re.fullmatch(regex, values[entry])):
                    st.error('Not valid email address!')
                    return False
                elif not self.check_available('email',values[entry]):
                    st.error('Email already exist!')
                    return False
        return True 

    def signup(self):
            ph=st.empty()
            new_user_form = ph.form('new_user_form')
            new_user_form.subheader('Sign up a new account')
            f_name = new_user_form.text_input('Full Name')
            user_name = new_user_form.text_input('User Name (required)')
            email = new_user_form.text_input('Email (required)')
            password = new_user_form.text_input('Password (required) more than 4 chars')
            r_passowrd = new_user_form.text_input('Repeat Password (required)')

            if new_user_form.form_submit_button('Sign Up'):    
                if len(user_name) and len(email) and len(password) and len(r_passowrd)>0:
                    if  self.validate({'user_name':user_name,'passwords':[password,r_passowrd],'email':email}): 
                        hashed_pw=stAuth.Hasher([password]).generate()[0]
                        try:
                            user_data=dict({
                                'name':f_name,
                                'user_name':user_name,
                                'email':email,
                                'password':hashed_pw,
                                'api_keys':{},
                                'account_type':'B',
                                'join_date':str(datetime.now().date())
                                
                            })
                            self.db_ref.add_new_user(user_data)
                            st.success('Registeration completed successfully, You canm log in from login section')
                            ph.text('')
                        except Exception as e:
                            st.error(e)    
                    else :
                        pass
                        st.warning('Register could not be completed, Try fix above errors!')    
                else :
                    st.error('required fields must not be empty ') 

    def logout(self):
        name=str(st.session_state['name']).replace(' ','+')
        st.sidebar.image(image=f"https://ui-avatars.com/api/?rounded=true&name={name}",caption=name.replace('+',' ').capitalize())
        if st.sidebar.button ('Logout', key='sidebar_btn_logout'):
            self.user_authenticated=False
            self.authenticator.cookie_manager.delete(self.cookie_name)
            st.session_state['logout'] = True
            st.session_state['name'] = None
            st.session_state['username'] = None
            st.session_state['email'] = None
            st.session_state['user_key'] = None
            st.session_state['authentication_status'] = None
            self.user_authenticated=False
            st.session_state['auth_object']=self
    def get_cook(self):
        data={'usernames':
                        {'m':{
                            'name': '',
                            'password':'',
                            'email':'',
                            'user_key':'',
                        }}
                    }
        self.authenticator=stAuth.Authenticate(credentials=self.users_dic,cookie_name='cookmook',key='any',cookie_expiry_days=30,preauthorized=[''])
        self.authenticator._check_cookie()
        if st.session_state.authentication_status:
            self.user_authenticated=True
    def login(self):
        name,authentication_status,username=self.authenticator.login('login',location='main')
        if st.session_state['authentication_status']:
                self.user_authenticated=True
                # st.session_state['auth_object']=self
                self.message="user has been authintecated at "+str(datetime.now())
                # self.authenticator.logout('Logout', 'sidebar')
                # st.write(f'Welcome *{name}*')
                # # st.title('Some content')
        elif authentication_status == False:
                self.user_authenticated=False
                # st.session_state['auth_object']=self
                self.message="user has been loged out  at "+str(datetime.now())
                st.error('Username/password is incorrect')
        elif authentication_status == None:
                self.user_authenticated=False
                # st.session_state['auth_object']=self
                self.message="user has no auth  at "+str(datetime.now())
                st.warning('Please enter your username and password')

    
