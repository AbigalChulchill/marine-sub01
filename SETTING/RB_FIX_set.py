import requests
import var_set

print("===========================")
print()
api_key = str(input("api_key = "))
api_secret = str(input("api_secret = "))
token = str(input("token = "))
print()
print("===========================")
print()
begin_money = str(input('Begin_money = '))
status = str(input('Do you want to START or TEST  ( S / T ) ? '))
A = input('Asset_RB = ')
asset_RB = str(A.upper())
print()
print("===========================")
print()
balance_fix = str(input('Balance_Fix = '))
print()
print("===========================")
print()
limit_percent = str(input('limit_percent = '))
print()
print("===========================")
print()
E = str(input("Do you want to check EMA  ( Y / N ) ?  "))

Ex = 0
EMAx = str(Ex)
print()
if E == "Y":
    EMAx = "Y"
    print(">>>>>","1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d")
    emat = str(input("Input EMA 10,40,65 TimeFrame = "))
else:
    EMAx = "N"
    emat = str(0)
print()
print("===========================")
print()
sav = str(input("Do you want to Auto saving ?  ( Y / N ) "))
print()
if sav == "Y" :
    as_sav = str(input("Mark SYMBOL to Auto-saving = " ))
    asset_saving = str(as_sav.upper())
    savx = str(input("setting Auto saving with value GROWTH or GROWTH% ?  ( G / GP ) "))
    savy = str(input("input value GROWTH or GROWTH% = "   ))
elif sav == "N" :
    asset_saving = str(0)
    savx = str(0)
    savy  = str(0)
else :
    print("saving error")
print()
print("===========================")
print()
td = str(input('sleep_date  = '))
th = str(input('sleep_hours = '))
tm = str(input('sleep_mins  = '))
print()
print("only Admin test")
ts = str(input('sleep_secs  = '))
print()
print("===========================")
print()
line = str(input("Do you want to line-notify only Real-Trade ?  ( Y / N ) "))
print()
print("===========================")
print()
show = str(input("Do you want to show sumary ?  ( Y / N ) "))

print()
progress = str(input("DO YOU WANT TO PROGRESS ROBOT ?  ( Y / N ) "))
print()
if progress == "Y":
    data_base = "/"+api_key+"/"+api_secret+"/"+token+"/"+begin_money+"/"+status+"/"+asset_RB+"/"+balance_fix+"/"+limit_percent+"/"+EMAx+"/"+emat+"/"+sav+"/"+asset_saving+"/"+savx+"/"+savy+"/"+line+"/"+td+"/"+th+"/"+tm+"/"+ts
    requests.post(url=var_set.domain+"/"+"RB_DYNAMIC"+data_base)
else :
    print("ROBOT_STOP")

