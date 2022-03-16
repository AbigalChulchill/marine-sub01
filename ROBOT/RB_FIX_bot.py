import time
import emoji
import ccxt
import numpy as np
import pandas as pd
import pandas_ta as ta
from songline import Sendline
from tabulate import tabulate
from datetime import datetime
from dateutil.relativedelta import relativedelta
from binance import Client
import smtplib


def rebalance_fix(api_key,api_secret,token,imail,ipass,remail,rec,begin_money,st,asset_RB,Balance_fix,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts,domain_name):
    
    exchange = ccxt.binance  ({'apiKey' : api_key ,'secret' : api_secret ,'enableRateLimit': True})

    saving = Client(api_key,api_secret)

    countdown = (td * 86400)+ (th * 3600) + (tm * 60) + ts

    symbolx = asset_RB+"/"+'USDT' #pair_trade

    if st == "S":
        status = str(1)
    elif st == "T":
        status = str(0)
    else :
        status = str(0)

    def int_port():

        now = datetime.today()
        local = now + relativedelta(hours=int(7),minutes=int(0))
        time1 = str(local.day)+"/"+str(local.month)+"/"+str(local.year)
        time2 = str(local.hour)+":"+str(local.minute)+":"+str(local.second)
        timex = time1 +"_"+ time2

        sig = "Signals"
        d = str(timex)
        symbol = asset_RB
        bal =  "-"
        pri = "-"
        mak = "-"
        volbs = "-"
        valbs = "-"
        fin = "-"
        g = "-"
        gp = "-"
        sav = "-"
        inter = "-"
        type = "FIX"
        begin = str(begin_money)
        sym_sav = str(asset_saving)

        gmail_user = imail
        gmail_password = ipass

        sent_from = gmail_user
        to = [remail]
        subject = 'Portfolio'
        body_x = sig+","+d+" , "+symbol+" , "+bal+" , "+pri+" , "+mak+" , "+volbs+" , "+valbs+" , "+fin+" , "+g+" , "+gp+" , "+sav+" , "+inter+" , "+type+" , "+begin+" , "+sym_sav

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
            print("Sending finish")
        except Exception as ex:
            print ("Something went wrong….",ex)

    def EMA_base():
        
        signal = []
       
        if EMAx == "Y":
            ohlcv = exchange.fetch_ohlcv(symbol = symbolx,timeframe=emat,limit=1000)
            data = pd.DataFrame(ohlcv, columns =['datetime', 'open','high','low','close','volume'])
            data['datetime']  = pd.to_datetime(data['datetime'], unit='ms')
            data.set_index('datetime', inplace=True)

            EMA1  = np.array(data.ta.ema(10))
            EMA2  = np.array(data.ta.ema(40))
            EMA3  = np.array(data.ta.ema(65))
            
            EMA1x = [EMA1[-1],EMA1[-2],EMA1[-3],EMA1[-4],EMA1[-5],EMA1[-6]]
            EMA2x = [EMA2[-1],EMA2[-2],EMA2[-3],EMA2[-4],EMA2[-5],EMA2[-6]]
            EMA3x = [EMA3[-1],EMA3[-2],EMA3[-3],EMA3[-4],EMA3[-5],EMA3[-6]]
            
            ema_set = np.stack( (EMA1x,EMA2x,EMA3x), axis=1 )

            EMA_base = []
            
            for j in range(len(ema_set)):
                a = ema_set[j][0]
                b = ema_set[j][1]
                c = ema_set[j][2]
                
                if a < b < c :
                    EMA_base.append("down")

                elif a > b > c :
                    EMA_base.append("up")
                
                else :
                    EMA_base.append("run")

            # กำหนดจุดสนใจ
            #--------------------trand
            if EMA_base[0] == EMA_base[1] == EMA_base[2] == EMA_base[3] == EMA_base[4] == EMA_base[5] == "down":
                signal.append("STOP_LO")
            elif EMA_base[0] == EMA_base[1] == EMA_base[2] == EMA_base[3] == EMA_base[4] == EMA_base[5] == "up":
                signal.append("STOP_UP")
            else :
                signal.append("RUNNING")
        
        else :
            signal.append("STOPPING")
    
        return  signal

    def Signal_Status():
    
        ema_signal = EMA_base()

        os = 0
        sx = []
        # os status 
        # 1 = เปิดการส่งคำสั่งซื้อขาย
        # 2 = Testing
        # 0 = ปิดการส่งคำสั่งซื้อขาย

        # STOP_UP ปิดการ ขายเมื่อราคากำลังเป็นขาขึ้น
        # STOP_LO 
        # RUNNING เส้น EMA ไม่อยู่ในเงื่อนไข ขาขึ้น หรือ ขาลง

        if EMAx == "Y":

            print("Signal_Status    > ",ema_signal[0])

            if ((status == 1) and (ema_signal[0] != "RUNNING")) :           # Stop action
                os = 0
           
            elif ((status == 1) and (ema_signal[0] == "RUNNING")) :         # action
                os += 1
            
            elif status == 0:                                              # Testing
                os += 2

            # signalx = ema_signal[0]                                     # portfolio & line
            s = ema_signal[0]  
            sx.append(s)
       
        elif EMAx == "N":   

            print("Signal_Status    > ","--OFF--")

            if status == 1:
                os += 1
            elif status == 0:
                os += 2

            s = "--OFF--"                                      # portfolio & line
            sx.append(s)

        
        if status == "1":
            print("Rebalance_Status > ","RUNNING SYSTEM")
        
        else :
            print("Rebalance_Status > ","TESTING SYSTEM")
        print()
        
        signalx = sx[0]
        
        return os,signalx

    def Balancef():

        # ประเมิน indicator and status --------------------------------------------------------------------
       
        def line_notify():

            pri = '%.4f'%price_A
            emoji_bs = emo[0]
            bs = str(buysell[0])
            vol = '%.4f'%(volume[0])

            if growth >= 0:
                eg = emoji.emojize(":chart_with_upwards_trend:", use_aliases=True)
            elif growth < 0:
                eg = emoji.emojize(":chart_with_downwards_trend:", use_aliases=True)

            line = []
            if osx == 0:
                line.append('Status     =    System_Stop')
            elif osx == 1:
                line.append('Status     =    System_Running')
            elif osx == 2:
                line.append('Status     =    System_Test')
            
            messenger = Sendline(token)
            messenger.sendtext(
                
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Domain     =    "+str(domain_name)+
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+"System     =    "+'Balance Fix'+
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Signal     =    "+str(signaly)+
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+str(line[0])+
                         
                '\n\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+'date  = ' +str(time1)+
                '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+'time  = '+str(time2)+
                '\n'+emoji_bs+str(bs)+' '+str(vol)+' '+str(asset_RB)+
                
                '\n\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'price     = '+str(pri)+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Vol.1     = '+str(vol1)+' '+str(asset_RB)+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Value.1  = '+str(value1)+' USD'+
                # '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'NAV.1    = '+str(navx)+' USD'+

                '\n\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Vol.2  = '+str(vol2)+' '+'USDT'+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Value.2  = '+str(value2)+' USD'+

                '\n\n'+(emoji.emojize(":moneybag:", use_aliases=True)*2)+'for fix '+str(Balance_fix)+' '+'USDT'+(emoji.emojize(":moneybag:", use_aliases=True)*2) +

                '\n\n'+emoji.emojize(":blue_book:", use_aliases=True)+'Asset_Sav  = '+str(asset_saving)+
                '\n'+emoji.emojize(":blue_book:", use_aliases=True)+'Value_Sav  = '+str(asset_sav)+
                '\n'+emoji.emojize(":blue_book:", use_aliases=True)+'Interest  = '+str(Interesty)+

                '\n\n'+emoji.emojize(":moneybag:", use_aliases=True)+'BeginMoney  = '+str(begin_money)+' USDT' +
                '\n'+eg+'Growth      = '+str(gro)+' USDT'+
                '\n'+eg+'Growth%     = '+str(gro_p)+"%"

                )

        def fin_port():

            sig = str(signaly)
            d = str(timex)
            symbol = asset_RB
            bal = str(Balance_fix)
            pri = str('%.4f'%price_A)
            mak = buysell[0]
            volbs = str('%.4f'%volume[0])
            valbs = str('%.4f'%value[0])
            fin = str('%.4f'%value_AB)
            g = str(gro)
            gp = str(gro_p)
            sav = str(asset_sav)
            inter = str(Interesty)
            type = "FIX"
            begin = str(begin_money)
            sym_sav = str(asset_saving)

            gmail_user = imail
            gmail_password = ipass

            sent_from = gmail_user
            to = [remail]
            subject = 'Portfolio'
            body = sig+","+d+" , "+symbol+" , "+bal+" , "+pri+" , "+mak+" , "+volbs+" , "+valbs+" , "+fin+" , "+g+" , "+gp+" , "+sav+" , "+inter+" , "+type+" , "+begin+" , "+sym_sav

            email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)

            try:
                smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                smtp_server.ehlo()
                smtp_server.login(gmail_user, gmail_password)
                smtp_server.sendmail(sent_from, to, email_text)
                smtp_server.close()
                print ("Email sent successfully!")
            except Exception as ex:
                print ("Something went wrong….",ex)

        osx,signaly = Signal_Status()

        # ประเมินก่อนซื้อขาย---------------------------------------------------------------------------------
        
        now = datetime.today()
        local = now + relativedelta(hours=int(7),minutes=int(0))
        time1 = str(local.day)+"/"+str(local.month)+"/"+str(local.year)
        time2 = str(local.hour)+":"+str(local.minute)+":"+str(local.second)
        timex = time1 +"_"+ time2
        print("  date   = ",time1,"\n"," time   = ",time2)

        # ตรวจสอบจำนวณเหรียญ -----------------------------------------------------------------------
        
        Get_balance = exchange.fetch_balance()
        volume_A = Get_balance [asset_RB] ['total'] #รอง
        Volume_B = Get_balance ['USDT'] ['total'] #หลัก
        print("Volume_A = " , '%.4f'%volume_A,asset_RB)
        print("Volume_B = " , '%.4f'%Volume_B,"USDT")

        # ราคาเหรียญ -----------------------------------------------------------------------
    
        get_price_A  = exchange.fetch_ticker(symbolx)
        price_A = get_price_A ['last'] 
        print("market price" ,str(asset_RB)," =",str('%.4f'%price_A))

        # รายการซื้อขาย------------------------------------------------------------------------------------
        
        # มูลค่าเหรียญใน PORT
        value_A = volume_A * price_A

        emo = []
        buysell = []
        volume = []
        value = []

        # Asset > fix ที่กำหนด
        if   value_A > float(Balance_fix) + (float(Balance_fix) * float(limit_percent)/100) :
            print("Fix Value ",str(asset_RB)," = ",str(Balance_fix),"USDT")
             
            different  = value_A - float(Balance_fix)
            final = different / price_A  #บอกจำนวนเหรียญที่ต้อง ขาย
            print("sell",'%.4f'%final,str(asset_RB))

            emo.append(emoji.emojize(":apple:", use_aliases=True))
            buysell.append("sell")
            volume.append(final)
            value.append(different)

            if osx == 1:
                try :
                    exchange.create_order(symbolx ,'market','sell',final)
                    
                except :
                    print("Value market less than 10 usd")
             
        # Asset < fix ที่กำหนด
        elif value_A < float(Balance_fix) - (float(Balance_fix) * float(limit_percent)/100) :
            print("Value_ ",str(asset_RB),"_Inport_<_",str(Balance_fix),"USDT")
            
            different  = float(Balance_fix) - value_A
            final = different / price_A  #บอกจำนวนเหรียญที่ต้อง ขาย
            print("buy",str('%.4f'%final),str(asset_RB))

            emo.append(emoji.emojize(":green_apple:", use_aliases=True))
            buysell.append("buy")
            volume.append(final)
            value.append(different)

            if osx == 1:
                try :
                    exchange.create_order(symbolx ,'market','buy',final)
                
                except :
                    print("Value market less than 10 usd")
                    
        else :
            emo.append(emoji.emojize(":x:", use_aliases=True))
            buysell.append("non")
            volume.append(0.0)
            value.append(0.0)
            print("None Trade") 

        # sumary get balance-----------------------------------------------------------------------------

        #ตรวจจำนวณเหรียญ ในบัญชี
        Get_balanceAA = exchange.fetch_balance()
        volume_AA = Get_balanceAA [(asset_RB)] ['total']
        volume_BB = Get_balanceAA ['USDT'] ['total']
        
        #ราคาเหรียญ
        get_priceAA  = exchange.fetch_ticker(symbolx)   
        price_AA = get_priceAA ['last'] 
        
        # มูลค่าเหรียญใน PORT
        value_AA = volume_AA * price_AA
        value_BB = volume_BB
        value_AB = value_AA + value_BB

        # ดึงข้อมูล Portfolio ที่ผ่านมา ----------------------------------------------------------------
        # ดึงเฉพาะ สถานะ initial & buy มาคำนวณ nav -------------------------------------------------
        # คำนวน growth + saving -------------------------------------------------------------------

        growthx = float(value_AB) - float(begin_money)                      # ตรวจ value ... มูลค่าใน port เพิ่มขึ้น กี่ USDT
        growth_perx = ( float(growthx) * 100 / float(begin_money) )         # ตรวจ value เพืามกี่ % ... USDT ที่เพื่มขึ้นใน พอท คิดเป็นกี่ % ของ begin money
    
        # Auto saving------------------------------------------------------------------------
        
        #จำนวนเหรียญ
        if asset_saving == "USDT" :
            vol_sav = float(growthx)
            
        elif asset_saving != "USDT" :
            #ราคาเหรียญ
            sym_sav = asset_saving+"/"+'USDT' #pair_trade
            price_sav  = exchange.fetch_ticker(sym_sav)   
            pri_sav = price_sav ['last'] 
            
            vol_sav = float(growthx / pri_sav)
           

        product = asset_saving +"/"+'001'

        if sav == "Y":

            if savx == "G":
                if growthx > float(savy):           # ฝากทั้งหมดเมื่อจับสัญญานได้
                    try :
                        saving.purchase_lending_product(productId = product, amount = vol_sav )
                    except :
                        print("Can't saving")
                else :
                    print("-OFF- SAVING Less than value config = ",'%.2f'%growthx," USDT")

            elif savx == "GP":
                if growth_perx > float(savy):           # ฝากทั้งหมดเมื่อจับสัญญานได้
                    try :
                        saving.purchase_lending_product(productId = product, amount = vol_sav )
                    except :
                        print("Can't saving")
                else :
                    print("-OFF- SAVING Less than value config  = ",'%.2f'%growth_perx,"%")

            else :
                print("value savx error")

        else:
            print("-OFF- SAVING")

        # ตรวจสอบ final saving---------------------------------------------------------------------
    
        fi_saving = saving.get_lending_position(asset = asset_saving)
        try :
            amo = float(fi_saving[0]['totalAmount'])
            Inter = float(fi_saving[0]['totalInterest'])

        except :
            amo = 0.00
            Inter = 0.00

        # คำนวน growth + saving (ผลรวม) ------------------------------------------------------------------------

        # หามูลค่า ของเหรียญที่ savใน port เฉพาะเหรียญที่เหลือก
        if asset_saving == "USDT" :
            
            val_savin = amo

        elif asset_saving != "USDT" :

            sym_s = asset_saving+"/"+'USDT' #pair_trade
            price_s  = exchange.fetch_ticker(sym_s)   
            pri_s = price_s ['last'] 

            val_savin = amo * float(pri_s)
        
        growth = growthx + float(val_savin)
        growth_per =( float(growth) * 100 )  / float(begin_money)
        gro = '%.2f'%growth
        gro_p = '%.2f'%growth_per

        asset_sav = '%.2f'%val_savin
        Interesty = '%.2f'%Inter

        # ส่งข้อมูลไปเก็บยัง port------------------------------------------------------------------
        
        if  rec == "Y" :

            if value[0] > 10 :
                fin_port()    
            else :
                print("-OFF- portfolio less than 10")

        elif rec == "N" :
            print("-OFF- portfolio Only Real-trade")
            fin_port() 

        else :
            print("Portfolio error by",rec)
        
        
        # ส่ง ค่าเป็นตาราง-----------------------------------------------------------------------

        vol1 = '%.4f'%volume_AA
        vol2 =  '%.4f'%volume_BB
        value1 =  '%.4f'%value_AA
        value2 =  '%.4f'%value_BB
        # navx = '%.2f'%nav
        
        info = {
            'Asset': [asset_RB,'USDT'], 
            'Volume': [vol1,vol2], 
            'Value': [value1,value2]}

        info2 = {
        
            'Growth': [str(gro)+' USDT'], 
            'Growth%': [str(gro_p)+' %']}
            
        print(tabulate(info, headers='keys', tablefmt='fancy_grid'))
        print(tabulate(info2, headers='keys', tablefmt='fancy_grid'))

        # ส่ง line---------------------------------------------------------------------------------
        if  line == "Y" :

            if value[0] > 10 :
                line_notify()    
            else :
                print("-OFF- LineNotify less than 10")

        elif line == "N" :
            print("-OFF- LineNotify Only Real-trade")
            line_notify()

        else :
            print("LineNotify error by",line)
        
        print("Sleep time !!")


    int_port()
    while True:
        Balancef()
        try:
            when_to_stop = abs(int(countdown))
        except:
            print("something error in sleep time")
            break
        while when_to_stop >= 0:
            m, s = divmod(when_to_stop, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
                            
            time_left = str(d).zfill(2)+"d" + ":" +str(h).zfill(2)+"h" + ":" + str(m).zfill(2)+"m" + ":" + str(s).zfill(2)+"s"
            print(time_left + "\r", end="")
            time.sleep(1)
            when_to_stop -= 1
        print()