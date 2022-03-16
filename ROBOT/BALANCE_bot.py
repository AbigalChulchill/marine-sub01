import emoji
import ccxt
from dateutil.relativedelta import relativedelta
from datetime import datetime
from songline import Sendline
from binance import Client

def total_spot(api_key,api_secret,token,domain_name):
    print("com in the room ")
    password = ""
    exchange = ccxt.binance  ({'apiKey' : api_key ,'secret' : api_secret ,'password' : password ,'enableRateLimit': True})
        
    Get_balance = exchange.fetch_balance()
    recive = Get_balance['info']
    
    out = list(recive.items())
    outx = out[9][1]
    
    sym_sum = []                                # fine all sym
    for i in range(len(outx)):
        sym = out[9][1][i]['asset']

        sym_sum.append(sym)
        
    total_balance = 0
    
    for i in range(len(sym_sum)):
        try :
            sym = sym_sum[i]
            sym_s = Get_balance [sym] ['total']            # ได้จำนวนเหรียญ แต่ละเหรียญ

            symbol = sym+"/"+'USDT' #pair_trade
            price_x  = exchange.fetch_ticker(symbol)
            price_y = price_x ['last']                     #  ได้ราคาเหรียญ

            price = float(sym_s) * price_y
            
            total_balance += price
        except:
            continue
    
    messenger = Sendline(token)
    messenger.sendtext(

        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Domain     =    "+str(domain_name)+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"TotalSPOT  =    "+str(total_balance)+" USDT")
        
def total_sym(api_key,api_secret,token,asset,domain_name):

    password = ""
    exchange = ccxt.binance  ({'apiKey' : api_key ,'secret' : api_secret ,'password' : password ,'enableRateLimit': True})
    sym = asset.upper()
    pair = sym+"/"+"USDT"
    
    # ตรวจสอบจำนวณเหรียญ -----------------------------------------------------------------------
    
    Get_balance = exchange.fetch_balance()
    Volume_A = Get_balance [sym] ['total'] #รอง
    Volume_B = Get_balance ['USDT'] ['total'] #หลัก

    # ราคาเหรียญ -----------------------------------------------------------------------

    get_price  = exchange.fetch_ticker(pair)
    price_A = get_price ['last'] 
    
    val = price_A * Volume_A
    total_pair = val + Volume_B

    messenger = Sendline(token)
    messenger.sendtext(

        '\n\n'+emoji.emojize(":bell:", use_aliases=True)+"Domain   =    "+str(domain_name)+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Vol."+str(sym)+"    =    "+str('%.4f'%Volume_A)+" coin"+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Vol."+"USDT"+"    =    "+str('%.4f'%Volume_B)+" coin"+

        '\n\n'+emoji.emojize(":bell:", use_aliases=True)+"Val."+str(sym)+"    =    "+str('%.4f'%val)+" USDT"+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Val."+"USDT"+"    =    "+str('%.4f'%Volume_B)+" USDT"+

        '\n\n'+emoji.emojize(":bell:", use_aliases=True)+"Sum_Value"+"    =    "+str('%.4f'%total_pair)+" USDT")

def saving_sym(api_key,api_secret,token,asset,domain_name):
   
    sym = asset.upper()
    log = Client(api_key,api_secret)
    data_in = log.get_lending_position(asset = str(sym))


    today_sav = float(data_in[0]['todayPurchasedAmount'])       #วันนี้ฝากไปเท่าไหร่
    total_vol = float(data_in[0]['totalAmount'])                   #จำนวนเหรียญฝากทั้งหมด
    total_inter = float(data_in[0]['totalInterest'])               #ดอกเบี้ยสะสม

    messenger = Sendline(token)

    sym_sav = sym+"/"+'USDT' #pair_trade
    exchange = ccxt.binance ({'apiKey' : api_key ,'secret' : api_secret  ,'enableRateLimit': True})

    price_sav  = exchange.fetch_ticker(sym_sav)   
    pri_sav = price_sav ['last'] 

    tvo = '%.4f'%total_vol
    
    tva = total_vol * pri_sav
    tvax = '%.4f'%tva
    ti = '%.4f'%total_inter


    messenger.sendtext(

        '\n\n'+emoji.emojize(":bell:", use_aliases=True)+"Domain       =    "+str(domain_name)+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Asset       =    "+str(sym)+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Today_sav    =    "+str(today_sav)+" coin"+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Total_Vol.  =    "+str(tvo)+" coin"+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Total_Val.  =    "+str(tvax)+" USDT"+
        '\n'+emoji.emojize(":bell:", use_aliases=True)+"Total_Interest    =    "+str(ti)+" USDT")

def saving_redeem(api_key,api_secret,token,asset,vol,domain_name):
    
    exchange = ccxt.binance ({'apiKey' : api_key ,'secret' : api_secret  ,'enableRateLimit': True})
    log = Client(api_key,api_secret)
    messenger = Sendline(token)

    now = datetime.today()
    local = now + relativedelta(hours=int(7),minutes=int(0))
    time1 = str(local.day)+"/"+str(local.month)+"/"+str(local.year)
    time2 = str(local.hour)+":"+str(local.minute)+":"+str(local.second)
    timex = time1 +" *** "+ time2

    sym = asset.upper()

    sym_sav = sym+"/"+'USDT' #pair_trade
    price_sav  = exchange.fetch_ticker(sym_sav)   
    pri_sav = price_sav ['last'] 
    
    product = sym+'001'
    volume = float(vol)

    vol_red = '%.4f'%volume
    var = volume * pri_sav 
    val_red = '%.4f'%var

    try :
        print("Redeem")
        
        log.redeem_lending_product(productId = product , amount = volume, type = 'NORMAL')

        messenger.sendtext(
            '\n\n'+emoji.emojize(":bell:", use_aliases=True)+"Domain       =    "+str(domain_name)+
            '\n'+emoji.emojize(":bell:", use_aliases=True)+"Date      =    "+str(timex)+
            '\n'+emoji.emojize(":bell:", use_aliases=True)+"Asset_Redeem       =    "+str(sym)+
            '\n'+emoji.emojize(":bell:", use_aliases=True)+"Redeem_Vol.  =    "+str(vol_red)+" coin"+
            '\n'+emoji.emojize(":bell:", use_aliases=True)+"Redeem_Val.  =    "+str(val_red)+" USDT")
   
    except :

        print("Error by Redeem")
        messenger.sendtext(

            '\n\n'+(emoji.emojize(":bell:", use_aliases=True)*2)+" Something error while Redeem "+(emoji.emojize(":bell:", use_aliases=True)*2))
            

    

