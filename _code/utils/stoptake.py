from ..models.Positioninfo import Positioninfo as Positioninfo
#stop loss logic
def checkstoploss(pi:Positioninfo,current_price,slpercent=1):

  isstopped=False
  # print("checking if stopped out pair",pi.pair)
  if pi !=None and  pi.openprice != '' and current_price != '' :
    trend=pi.ptype
    openprice=float(pi.openprice)
    currentprice=float(current_price)
    
    slpercent=slpercent*-1
    pricecchangeshort=((openprice-currentprice)/openprice)*100
    pricecchangeshort=round(pricecchangeshort,2)
    pricecchangelong=((currentprice-openprice)/openprice)*100
    pricecchangelong=round(pricecchangelong,2)
    plValueshort=pricecchangeshort*pi.size/100
    plValuelong=pricecchangelong*pi.size/100

    if  trend=='Sell' and  pricecchangeshort <= slpercent:
      # print(">>>> stop Loss   |SHORT|",pi.pair.upper()," | price change %",pricecchangeshort," | SL %:", slpercent)
      isstopped=True 
    elif trend=='Buy' and pricecchangelong <= slpercent : 
      # print(">>>> stop Loss   |LONG |",pi.pair.upper()," | price change %",pricecchangelong," | SL %:", slpercent)
      isstopped=True
    # else:
    #   if trend=='short':
    #    print(pi.pair,"  short poisition p/l %=",pricecchangeshort,"Value ",plValueshort)
    #   else:
    #    print(pi.pair,"  Long poisition p/l %=",pricecchangelong,"Value=",plValuelong)
  return isstopped 


def checktakeProfit(pi:Positioninfo,current_price,TPpercent=2):

  isstopped=False
  # print("checking if taking profit out")
  if pi !=None and  pi.openprice != 0 and current_price != 0 :
    trend=pi.ptype
    openprice=float(pi.openprice)
    currentprice=float(current_price)
    
    
    pricecchangeshort=((openprice-currentprice)/openprice)*100
    pricecchangeshort=round(pricecchangeshort,2)
    pricecchangelong=((currentprice-openprice)/openprice)*100
    pricecchangelong=round(pricecchangelong,2)
    plValueshort=pricecchangeshort*pi.size/100
    plValuelong=pricecchangelong*pi.size/100

    if  trend=='Sell' and  pricecchangeshort >= TPpercent:
      # print(">>>> take proift |SHORT|",pi.pair.upper()," | price change %",pricecchangeshort," | tp %:", TPpercent)
      # print("price change %",pricecchangeshort," tp %:", TPpercent)
      isstopped=True 
    elif trend=='Buy' and pricecchangelong >= TPpercent : 
      # print(">>>> take proift |LONG | ",pi.pair.upper(),"| price change %",pricecchangelong," | tp %:", TPpercent)
      # print("price change %",pricecchangelong," tp %:", TPpercent)
      isstopped=True
    else:
      if trend=='short':
      #  print(pi.pair," :short p/l=",pricecchangeshort,"% | Value= ",plValueshort)
        pass
      else:
        # print(pi.pair,"Long p/l=",pricecchangelong,"% | Value= ",plValuelong)
        pass
  return isstopped 

