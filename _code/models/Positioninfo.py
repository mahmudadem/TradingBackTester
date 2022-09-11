

class Positioninfo :
    # number,pair,ptype,size,opendate,openprice,closeprice,closedate,isclosed,closetype,pl,exchange,qty,isAlive,executions,t4h=0,"","",0,"",0,0,"",False,"","","","","","",""
    # tp,sl=0,0
    def __init__(self,number=0,pair="",ptype="",size=1000,opendate="",tp=6,sl=2.5,
                     openprice=0.0,closeprice=0.0,closedate="",isclosed=False,closetype="",pl=0.0,exchange="BB",qty=0.0,isAlive=False,executions=None,id=""):
        self.number=number
        self.pair=pair
        self.ptype=ptype
        self.size=size
        self.opendate=opendate
        self.openprice=openprice
        self.closeprice=closeprice
        self.closedate=closedate
        self.isclosed=isclosed
        self.closetype=closetype
        self.pl=pl
        self.exchange=exchange
        self.qty=qty
        self.isAlive=isAlive
        self.id=id
        
        self.tp=tp
        self.sl=sl
        if executions is None:
            self.executions=''
        else:
            self.executions=executions    
