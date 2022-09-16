class exchange:
    def __init__(self,name,pub_key,secret_key,dataStucter={}) -> None:
        self.name=name
        self.pub_key=pub_key
        self.secret=secret_key
        self.data_structer=dataStucter
        self.id='1'

    def get_info(self):
        return {
            self.name:{
                'id':self.id,
                'pub_key':self.pub_key,
                'secret': self.secret,
                }
        }
