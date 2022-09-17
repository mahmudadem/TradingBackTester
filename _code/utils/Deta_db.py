
from deta import Deta
import os
from .exceptions import CredentialsError, ResetError, RegisterError, ForgotError, UpdateError
# os.environ['API_KEY'] = 'a0j6239f_Tu6tSaLmsc8t7RoaWh343FW6aTBc1f9Z'
cts={'name':'full_name','User Name':'user_name','email':'email'}
os.environ['API_USER'] = 'khaled'
class deta_db:
    def __init__(self,db_name,key=None) -> None:
        self.db_name=db_name
        env_key=os.getenv('API_KEY') if os.getenv('API_KEY')!=None else ''
        self.connection=Deta(key if key is not None else env_key)
        self.connect()
    def connect(self):
        self.db = self.connection.Base(self.db_name)

    def create():
        pass


class user_db(deta_db):
    def __init__(self,db_name='users') -> None:
        super().__init__(db_name)
        self.db = self.connection.Base(db_name)

    def add_new_user(self,data: dict):
        check_userName=self.get_user_field(_feild='user_name',_value=data['user_name'])
        check_email=self.get_user_field(_feild='email',_value=data['email'])
        if check_userName.count >0 :
            raise RegisterError("user name already exist")
        if check_email.count >0:
            raise RegisterError("Email already exist")    
        self.db.insert(data=data)

    def delete(self,keys: list):
        for key in keys:
            self.db.delete(key)

    def update(self,data: dict,user_key):
        
        try:
            if user_key:
                self.db.update(data,key=user_key)
                return True
            else :
                False 
        except Exception as e:
            print(e)
            return False        
    
    def get_user_field(self,_feild,_value,key=None):
        query={'key':key,_feild:_value} if key !=None else {_feild:_value}
        return  self.db.fetch(query=query)

    def fetch(self,query: dict):
        return self.db.fetch(query=query)

    def check_api_data_exist(self,user_key,key_name,ex_name):
        data=self.db.fetch({'key':user_key}).items[0]['api_keys'].items()
        for name,keys in data:
            if name==key_name and keys['ex_name']==ex_name:
                    return True
            
        return False


    def add_api_keys(self,user_key,key_name,ex_name,pub,sec):

        newValue=dict({
                        "ex_name": ex_name,
                        "pub_key": pub,
                        "secret":sec
                    })

        apis=self.db.fetch({'key':user_key}).items[0]['api_keys'] 
        apis[key_name]=newValue
        try:
            self.db.update(updates={'api_keys':apis},key=user_key)
            return True
        except :
            return False    
        print(apis)     
