import emoji
import ccxt
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

        '\n\n'+emoji.emojize(":wrench:", use_aliases=True)+"Domain   =    "+str(domain_name)+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Vol."+str(sym)+"    =    "+str('%.4f'%Volume_A)+" coin"+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Vol."+"USDT"+"    =    "+str('%.4f'%Volume_B)+" coin"+

        '\n\n'+emoji.emojize(":wrench:", use_aliases=True)+"Val."+str(sym)+"    =    "+str('%.4f'%val)+" USDT"+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Val."+"USDT"+"    =    "+str('%.4f'%Volume_B)+" USDT"+

        '\n\n'+emoji.emojize(":wrench:", use_aliases=True)+"Sum_Value"+"    =    "+str('%.4f'%total_pair)+" USDT")

def saving_sym(api_key,api_secret,token,asset,domain_name):
   
    sym = asset.upper()
    log = Client(api_key,api_secret)
    data_in = log.get_lending_position(asset = str(sym))

    today_sav = float(data_in[0]['todayPurchasedAmount'])          #วันนี้ฝากไปเท่าไหร่
    total_sav = float(data_in[0]['totalAmount'])                   #จำนวนเหรียญฝากทั้งหมด
    total_inter = float(data_in[0]['totalInterest'])               #ดอกเบี้ยสะสม

    messenger = Sendline(token)
    messenger.sendtext(

        '\n\n'+emoji.emojize(":wrench:", use_aliases=True)+"Domain       =    "+str(domain_name)+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Today_sav    =    "+str(today_sav)+" USDT"+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Total_inter  =    "+str(total_sav)+" USDT"+
        '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Total_sav    =    "+str(total_inter)+" USDT")

