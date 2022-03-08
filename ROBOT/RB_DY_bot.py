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

def rebalance_dynamic(api_key,api_secret,token,begin_money,status,asset_RB,low_gap,zone_1,mid_gap,zone_2,high_gap,zone_3,zone_4,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts):

    password = ""
    exchange = ccxt.binance  ({'apiKey' : api_key ,'secret' : api_secret ,'password' : password ,'enableRateLimit': True})
    saving = Client(api_key,api_secret)
    messenger = Sendline(token)

    countdown = (td * 86400)+ (th * 3600) + (tm * 60) + ts

    symbolx = asset_RB+"/"+'USDT' #pair_trade

    def initial():

        z1 = 100 - int(zone_1)
        z2 = 100 - int(zone_2)
        z3 = 100 - int(zone_3)
        z4 = 100 - int(zone_4)

        messenger = Sendline(token)
        messenger.sendtext(
            '\n\n'+emoji.emojize(":wrench:", use_aliases=True)+"System     =    "+'Review RB_Ratio(d)'+
   
            "\n\nRatio 4 = "+str(zone_4)+"/"+str(z4)+
            "\n------------------ High gap = "+str(high_gap)+
            "\nRatio 3 = "+str(zone_3)+"/"+str(z3)+
            "\n------------------ mid gap = "+str(mid_gap)+
            "\nRatio 2 = "+str(zone_2)+"/"+str(z2)+
            "\n------------------ low gap = "+str(low_gap)+
            "\nRatio 1 = "+str(zone_1)+"/"+str(z1)+"\n")
            
    def EMA_base():
        
        signal = []
            
        if emat == "1":
            timef = emat
            ohlcv = exchange.fetch_ohlcv(symbol = symbolx,timeframe=timef,limit=1000)
            data = pd.DataFrame(ohlcv, columns =['datetime', 'open','high','low','close','volume'])
            data['datetime']  = pd.to_datetime(data['datetime'], unit='ms')
            data.set_index('datetime', inplace=True)

            EMA1  = np.array(data.ta.ema(10))
            EMA2  = np.array(data.ta.ema(40))
            EMA3  = np.array(data.ta.ema(65))
            
            EMA1x = [EMA1[-1],EMA1[-2],EMA1[-3],EMA1[-4],EMA1[-5],EMA1[-6]]
            EMA2x = [EMA2[-1],EMA2[-2],EMA2[-3],EMA2[-4],EMA2[-5],EMA2[-6]]
            EMA3x = [EMA3[-1],EMA3[-2],EMA3[-3],EMA3[-4],EMA3[-5],EMA3[-6]]
            
            EMAx = np.stack( (EMA1x,EMA2x,EMA3x), axis=1 )

            EMA_base = []
            
            for j in range(len(EMAx)):
                a = EMAx[j][0]
                b = EMAx[j][1]
                c = EMAx[j][2]
                
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
        print()
        ema_signal = EMA_base()

        os = 0
        # os status 
        # 1 = เปิดการส่งคำสั่งซื้อขาย
        # 2 = Testing
        # 0 = ปิดการส่งคำสั่งซื้อขาย

        # STOP_UP ปิดการ ขายเมื่อราคากำลังเป็นขาขึ้น
        # STOP_LO 
        # RUNNING เส้น EMA ไม่อยู่ในเงื่อนไข ขาขึ้น หรือ ขาลง

        if EMAx == "1":
            print("Signal_Status    > ",ema_signal[0])

            if ((status == 1) and (ema_signal[0] != "RUNNING")) :           # Stop action
                os = 0
           
            elif ((status == 1) and (ema_signal[0] == "RUNNING")) :         # action
                os += 1
            
            elif status == 0:                                              # Testing
                os += 2

            signalx = ema_signal[0]                                     # portfolio & line
       
        elif EMAx == "0":   
            print("Signal_Status    > ","--OFF--")

            if status == 1:
                os += 1
            elif status == 0:
                os += 2

            signalx = ("--OFF--")                                      # portfolio & line
        
        if status == "1":
            print("Rebalance_Status > ","RUNNING SYSTEM")
        
        else :
            print("Rebalance_Status > ","TESTING SYSTEM")
        print()

        return os,signalx

    def Balancec():

        # ประเมิน indicator and status --------------------------------------------------------
    
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
            if os == 0:
                line.append('Status     =    System_Stop')
            elif os == 1:
                line.append('Status     =    System_Running')
            elif os == 2:
                line.append('Status     =    System_Test')
                
            messenger = Sendline(token)
            messenger.sendtext(

                '\n'+emoji.emojize(":wrench:", use_aliases=True)+"System     =    "+'Balance Ratio(d)'+
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+"Signal     =    "+str(signalx)+
                '\n'+emoji.emojize(":wrench:", use_aliases=True)+str(line[0])+
                
                '\n\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+'date  = ' +str(time1)+
                '\n'+emoji.emojize(":alarm_clock:", use_aliases=True)+'time  = '+str(time2)+
                '\n'+emoji_bs+str(bs)+' '+str(vol)+' '+str(asset_RB)+
                
                '\n\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'price     = '+str(pri)+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Vol.1     = '+str(vol1)+' '+str(asset_RB)+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Value.1  = '+str(value1)+' USD'+
                # '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'NAV.1    = '+str(navx)+' USD'+

                '\n\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Vol.2     = '+str(vol2)+' USDT'+
                '\n'+emoji.emojize(":open_file_folder:", use_aliases=True)+'Value.2  = '+str(value2)+' USD'+

                '\n\n'+(emoji.emojize(":moneybag:", use_aliases=True)*2)+'for  '+str(coin_per)+' / '+str(usdt_per)+' % '+(emoji.emojize(":moneybag:", use_aliases=True)*2)+

                '\n\n'+emoji.emojize(":blue_book:", use_aliases=True)+'All Saving  = '+str(amounty)+
                '\n'+emoji.emojize(":blue_book:", use_aliases=True)+'Interest  = '+str(Interesty)+

                '\n\n'+emoji.emojize(":moneybag:", use_aliases=True)+'BeginMoney  = '+str(begin_money)+' USDT' +
                '\n'+eg+'Growth      = '+str(gro)+' USDT'+
                '\n'+eg+'Growth%     = '+str(gro_p)+"%"

                )

        def val_sav():
            if asset_saving == asset_RB :
                val_saving = amounty * price_AA

            elif asset_saving != asset_RB :
                price  = exchange.fetch_ticker(symbolx)   
                price_sav = (price ['bid'] + price ['ask'] )/2
                val_saving = amounty * price_sav
            
            elif asset_saving == 'USDT' :
                val_saving = amounty
            
            return val_saving
        
        os,signalx = Signal_Status()
        
        # ประเมินก่อนซื้อขาย --------------------------------------------------------------------
        
        now = datetime.today()
        local = now + relativedelta(hours=int(7),minutes=int(0))
        time1 = str(local.day)+"/"+str(local.month)+"/"+str(local.year)
        time2 = str(local.hour)+":"+str(local.minute)+":"+str(local.second)
        print("  date   = ",time1,"\n"," time   = ",time2)

        # ตรวจสอบจำนวณเหรียญ -----------------------------------------------------------------------
        
        Get_balance = exchange.fetch_balance()
        Volume_A = Get_balance [asset_RB] ['total'] #รอง
        Volume_B = Get_balance ['USDT'] ['total'] #หลัก
        print("Volume_A = " , '%.4f'%Volume_A,asset_RB)
        print("Volume_B = " , '%.4f'%Volume_B,"USDT")

        # ราคาเหรียญ -----------------------------------------------------------------------
    
        get_price_A  = exchange.fetch_ticker(symbolx)
        price_A = get_price_A ['last'] 
        print("market price" ,str(asset_RB)," =",str('%.4f'%price_A))

        # หาzone ของเหรียญ -----------------------------------------------------------------------
    
        if price_A <= int(low_gap) :
            coin_per = int(zone_1)
            usdt_per = 100 - coin_per
        elif int(low_gap) < price_A <= int(mid_gap) :
            coin_per = int(zone_2)
            usdt_per = 100 - coin_per
        elif int(low_gap) < int(mid_gap) < price_A <= int(high_gap) :
            coin_per = int(zone_3)
            usdt_per = 100 - coin_per
        elif int(low_gap) < int(mid_gap) < int(high_gap) < price_A :
            coin_per = int(zone_4)
            usdt_per = 100 - coin_per
        print("Dinamic_percent " ,str(coin_per),"/",str(usdt_per))
        print()

        # รายการซื้อขาย -----------------------------------------------------------------------
            
        # มูลค่าเหรียญ ใน port
        value_A = Volume_A * price_A
        value_B = Volume_B * 1

        emo = []
        buysell = []
        volume = []
        value = [] 

        #คำนวณ % เป็นมูลค่าที่ต้องมีใน port
        balance_coin   = (  (  float(value_A) + float(value_B) ) *  coin_per ) / 100

        # market -----------------------------------------------------------------------
    
        if  value_A > balance_coin + (balance_coin*float(limit_percent)/100) :
            print("Value_",str(asset_RB),"_Inport_>_",str(coin_per),"% ")
            
            different  = value_A - balance_coin
            final = different/price_A
            print("sell",str('%.4f'%final),str(asset_RB))

            emo.append(emoji.emojize(":apple:", use_aliases=True))
            buysell.append("sell")
            volume.append(final)
            value.append(different)

            if os == 1:
                try :
                    exchange.create_order(symbolx ,'market','sell',final)
                    
                except :
                    print("Value market less than 10 usd")
        
            
        elif value_A < balance_coin - (balance_coin*float(limit_percent)/100):
            print("Value_",str(asset_RB),"_Inport_<_",str(coin_per),"% ")
            
            different  = balance_coin - value_A
            final = different/price_A
            print("buy",str('%.4f'%final),str(asset_RB))

            emo.append(emoji.emojize(":green_apple:", use_aliases=True))
            buysell.append("buy")
            volume.append(final)
            value.append(different)
            
            if os == 1:
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

        # sumary get balance ----------------------------------------------------------------
    
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

        growthx = value_AB - float(begin_money)
        growth_perx = ( float(growthx) * 100 / float(begin_money) )
    
        # Auto saving------------------------------------------------------------------------
        
        product = asset_saving +"/"+'001'

        if sav == "y":

            if savx == "g":
                if growthx > float(savy):           # ฝากทั้งหมดเมื่อจับสัญญานได้
                    try :
                        exchange.purchase_lending_product(productId = product, amount = float(savy))
                    except :
                        print("Can't saving")
                else :
                    print("-OFF- SAVING Less than value config")

            elif savx == "gp":
                if growth_perx > float(savy):           # ฝากทั้งหมดเมื่อจับสัญญานได้
                    try :
                        exchange.purchase_lending_product(productId = product, amount = float(savy))
                    except :
                        print("Can't saving")
                else :
                    print("-OFF- SAVING Less than value config")

            else :
                print("value savx error")

        else:
            print("-OFF- SAVING")

        # final saving------------------------------------------------------------------------
    
        fi_saving = saving.get_lending_position(asset = asset_saving)
        try :
            amounty = str(fi_saving[0]['totalAmount'])
            Interesty = str(fi_saving[0]['totalInterest'])
        except :
            amounty = 0.00
            Interesty = 0.00

        # คำนวน growth + saving ------------------------------------------------------------------------

        value_saving = val_sav()
        
        growth = float(value_AB) - float(begin_money) + value_saving
        growth_per =( float(growth) * 100 )  / float(begin_money)
        gro = '%.2f'%growth
        gro_p = '%.2f'%growth_per
        
        # ส่งข้อมูลไปเก็บยัง port------------------------------------------------------------------
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
        if  line == "y" :

            if value[0] > 10 :
                line_notify()    
            else :
                print("-OFF- LineNotify less than 10")

        elif line == "n" :
            print("-OFF- LineNotify Only Real-trade")

        else :
            print("LineNotify error by",line)

    initial()
    while True:
        Balancec()
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








