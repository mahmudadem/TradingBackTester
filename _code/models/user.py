from exchange import exchange

class User:
    def __init__(self,full_name,username,email,password,api_keys:exchange,join_date,account_type) -> None:
        self.full_name=full_name
        self.email=email
        self.user_name=username
        self.password=password
        self.api_keys=api_keys
        self.join_date=join_date
        self.account_type=account_type

    def get_info(self):
        return {
                'first_name':self.full_name,
                'email':self.email,
                'user_name':self.user_name,
                'password':self.password,
                'api_keys':self.api_keys,
                'join_date':self.join_date,
                'account_type':self.account_type,
        }    