import ccxt
import time
import pandas as pd
import pandas_ta as ta
import numpy as np
import emoji
from songline import Sendline
from datetime import datetime
from dateutil.relativedelta import relativedelta
import SETTING.var_set as var_set
import smtplib


def tracker(api_key,api_secret,token,imail,ipass,remail,asset_RB,ind_t,e1,e2,e3,e4,r,b1,b2,m1,m2,m3,s1,s2,s3,s4,td,th,tm,ts,domain_name):

    countdown = (int(td) * 86400)+ (int(th) * 3600) + (int(tm) * 60) + int(ts)
    
    def track_run():
        
        password = ""
        exchange = ccxt.binance  ({'apiKey' : api_key ,'secret' : api_secret ,'password' : password ,'enableRateLimit': True})
        
        # ดึงข้อมูล
        symbolx = asset_RB+"/"+'USDT' #pair_trade
        
        ohlcv = exchange.fetch_ohlcv(symbol = symbolx ,timeframe=ind_t , limit=1000)
        data = pd.DataFrame(ohlcv, columns =['datetime', 'open','high','low','close','volume'])
        data['datetime']  = pd.to_datetime(data['datetime'], unit='ms')
        data.set_index('datetime', inplace=True)

        # =========================================================================
        now = datetime.today()
        
        nextA = now + relativedelta(hours=int(0),minutes=int(0))
        A1 = str(nextA.day)+"/"+str(nextA.month)+"/"+str(nextA.year)
        A2 = str(nextA.hour)+":"+str(nextA.minute)+":"+str(nextA.second)
        utc = str(A1)+" *** "+str(A2)

         # Grayscale Bitcoin , MicroStrategy
        nextB = now + relativedelta(hours=int(-5),minutes=int(0))
        B1 = str(nextB.day)+"/"+str(nextB.month)+"/"+str(nextB.year)
        B2 = str(nextB.hour)+":"+str(nextB.minute)+":"+str(nextB.second)
        t00500 = str(B1)+" *** "+str(B2)

         # Italy    Belgium
        nextC = now + relativedelta(hours=int(1),minutes=int(0))
        C1 = str(nextC.day)+"/"+str(nextC.month)+"/"+str(nextC.year)
        C2 = str(nextC.hour)+":"+str(nextC.minute)+":"+str(nextC.second)
        t0100 = str(C1)+" *** "+str(C2)

          #   India
        nextD = now + relativedelta(hours=int(5),minutes=int(30))
        D1 = str(nextD.day)+"/"+str(nextD.month)+"/"+str(nextD.year)
        D2 = str(nextD.hour)+":"+str(nextD.minute)+":"+str(nextD.second)
        t0530 = str(D1)+" *** "+str(D2)


        #  Thailand , Vietnam
        nextE = now + relativedelta(hours=int(7),minutes=int(0))
        E1 = str(nextE.day)+"/"+str(nextE.month)+"/"+str(nextE.year)
        E2 = str(nextE.hour)+":"+str(nextE.minute)+":"+str(nextE.second)
        t0700 = str(E1)+" *** "+str(E2)
        
      
        #  Malaysia  Philippines  Hong Kong
        nextF = now + relativedelta(hours=int(8),minutes=int(0))
        F1 = str(nextF.day)+"/"+str(nextF.month)+"/"+str(nextF.year)
        F2 = str(nextF.hour)+":"+str(nextF.minute)+":"+str(nextF.second)
        t0800 = str(F1)+" *** "+str(F2)
        
        # South Korea
        nextG = now + relativedelta(hours=int(9),minutes=int(0))
        G1 = str(nextG.day)+"/"+str(nextG.month)+"/"+str(nextG.year)
        G2 = str(nextG.hour)+":"+str(nextG.minute)+":"+str(nextG.second)
        t0900 = str(G1)+" *** "+str(G2)

        # ========================================================================

        get_price_A  = exchange.fetch_ticker(symbolx)
        price_A = get_price_A ['last']

        # ========================================================================

        EMA1  = data.ta.ema(int(e1))
        EMA2  = data.ta.ema(int(e2))
        EMA3  = data.ta.ema(int(e3))
        EMA4  = data.ta.ema(int(e4))

        EMAx = [{"EMA":int(e1),"PRICE":EMA1[-1]},{"EMA":int(e2),"PRICE":EMA2[-1]},{"EMA":int(e3),"PRICE":EMA3[-1]},{"EMA":int(e4),"PRICE":EMA4[-1]}]

        def fillin( friend ):
            return friend["PRICE"]

        EMAx.sort(key=fillin)

        a = str(EMAx[0]["EMA"])
        b = str(EMAx[1]["EMA"])
        c = str(EMAx[2]["EMA"])
        d = str(EMAx[3]["EMA"])

        ema_status = a + "," + b + "," + c + "," + d

        # ================================================================
        RSIx = np.array(data.ta.rsi(int(r)))

        rsi = '%.2f'%RSIx[-1]
    
        # ================================================================
        BBANDx = np.array(data.ta.bbands(length=int(b1), std=int(b2)))

        u = BBANDx[-1][2]
        m = BBANDx[-1][1]
        l = BBANDx[-1][0]

        low_per = '%.2f'%(((m - l) * 100 / m))+"%"
        up_per = '%.2f'%(((u - m) * 100 / m))+"%"

        # ================================================================

        MACDx = np.array(data.ta.macd(fast=int(m1), slow=int(m2), signal=int(m3)))

        fast = '%.2f'%MACDx[-1][0]
        macd = '%.2f'%MACDx[-1][1]
        slow = '%.2f'%MACDx[-1][2]

        # ================================================================

        STOx = np.array(data.ta.stochrsi(length=int(s1), rsi_length=int(s2), k=int(s3), d=int(s4)))

        kblue = '%.2f'%STOx[-1][0]
        dred = '%.2f'%STOx[-1][1]

        # ================================================================

        tx = str(t0700)
        sym = symbolx
        ema = ema_status
        rx = str(rsi)
        bbandx = str(up_per)+"/"+str(low_per)
        macdx = str(macd)+"/"+str(fast)+"/"+str(slow)
        stox = str(kblue)+"/"+str(dred)
        
        gmail_user = imail
        gmail_password = ipass

        sent_from = gmail_user
        to = [remail]
        subject = 'TRACKER'
        body_x = tx+" , "+sym+" , "+ema+" , "+rx+" , "+bbandx+" , "+macdx+" , "+stox

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body_x)

        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, email_text)
            smtp_server.close()
            # print ("Email sent successfully!")

        except Exception as ex:
            print ("Something went wrong….",ex)


        # ================================================================
        
        messenger = Sendline(token)
      
        messenger.sendtext(

            '\n'+emoji.emojize(":wrench:", use_aliases=True)+"DOMAIN     =    "+str(domain_name)+
            '\n'+emoji.emojize(":wrench:", use_aliases=True)+"SYSTEM     =    "+'ROBOT_TRACKER'+

            '\n\n'+str(utc)+ " ---> " +"UTC"+ 

            '\n\n'+emoji.emojize(":earth_americas:", use_aliases=True)+"Grayscale Bitcoin , MicroStrategy" +
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t00500) + " (-5) " +
            
            '\n\n'+emoji.emojize(":earth_asia:", use_aliases=True)+"IT,BE"+
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t0100) + " (+1)"+
            '\n'+emoji.emojize(":earth_asia:", use_aliases=True)+"IN"+
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t0530) + " (+5:30)"+
            '\n'+emoji.emojize(":earth_asia:", use_aliases=True)+"TH,VNM"+
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t0700) + " (+7)"+
            '\n'+emoji.emojize(":earth_asia:", use_aliases=True)+"MY,PH,HK"+
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t0800) + " (+8)"+
            '\n'+emoji.emojize(":earth_asia:", use_aliases=True)+"SKR"+
            '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+str(t0900) + " (+9)"+

            '\n\n'+"SYMBOL    =    " + str(symbolx)+
            '\n'+"TIMEFRAME    =    " + str(ind_t)+

            '\n\n'+"======="+" SETTING "+"======="+

            '\n\n'+"EMA    =    " + str(e1) +" / "+ str(e2) +" / "+ str(e3) +" / "+ str(e4)+
            '\n'+"RSI    =    " + str(r)+ 
            '\n'+"BBAND    =    " +"Length"+str(b1) +" / "+"std"+ str(b2)+
            '\n'+"MACD    =    " +"fast"+str(m1) +" / "+"slow"+str(m2) + " / "+"signal"+str(m3)+
            '\n'+"STORSI    =    " +"length"+str(s1) +" / "+"rsi"+str(s2) +" / "+"k"+str(s3) +" / "+"d"+str(s4)+

            '\n\n'+"======="+" NEWS "+"======="+

            '\n\n'+"PRICE SYMBOL    =    " + str(price_A)+ 
           
            '\n\n'+"EMA STATUS    =    " + str(ema_status)+ 

            '\n\n'+"RSI STATUS    =    " + str(rsi)+ 

            '\n\n'+"BBAND% UP    =    " + str(up_per) +
            '\n'+"BBAND% LO    =    " + str(low_per) + 

            '\n\n'+"MACD STATUS    =    " +str(macd)  +
            '\n'+"FAST STATUS    =    " +str(fast)  +
            '\n'+"SLOW STATUS    =    " +str(slow)  +
            
            '\n\n'+"STO K    =    " +str(kblue)  +
            '\n'+"STO D    =    " +str(dred)

            )
        
        print("END of ROBOT")

    while True :
        track_run()
        time.sleep(countdown)

    






    

























