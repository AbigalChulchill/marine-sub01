import imaplib
import email
from tabulate import tabulate


# body_x = "trend"+","+"date"+","+"symbol"+","+"ratio"+","+"price"+","+"market"+","+"volBS"+","+"valBS"+","+"final_value"+","+"growth"+","+"growth_rate"+","+"SavingAll"+","+"interest"

def log():
    # email,password,rmail,keep
    #credentials
    username = "robot.portfolio.01@gmail.com"

    #generated app password
    app_password= "@01portfolio"

    # https://www.systoolsgroup.com/imap/
    gmail_host= 'imap.gmail.com'

    #set connection
    mail = imaplib.IMAP4_SSL(gmail_host)

    #login
    mail.login(username, app_password)

    #select inbox
    mail.select("INBOX")

    #select specific mails
    find = "FROM " + str("harith.detbun@gmail.com")
    print(find)
    _, selected_mails = mail.search(None, find)

    #total number of mails from specific user
    print("Portfolio",find, len(selected_mails[0].split()))

    signal = []
    date = []
    symbol = []
    ratio = []
    price = []
    market = []
    vol = []
    val = []
    final = []
    growth = []
    growth_per = []
    saving = []
    interest = []

    out = []

    for i in selected_mails[0].split():
        _, data = mail.fetch(i , '(RFC822)')
        _, bytes_data = data[0]

        #convert the byte data to message
        email_message = email.message_from_bytes(bytes_data)

        
        for j in email_message.walk():
            # body_x = "trend"+","+"date"+","+"symbol"+","+"ratio"+","+"price"+","+"market"+","+"volBS"+","+"valBS"+","+"final_value"+","+"growth"+","+"growth_rate"+","+"SavingAll"+","+"interest"

            if j.get_content_type()=="text/plain" or j.get_content_type()=="text/html":
                message = j.get_payload(decode=True)
                mes =  message.decode()
                tex = mes.split("\n")
                del_r = tex[0] 
                text = del_r.replace('\r', "")
                x = text[8:]
                y = x.split(",")
                print(y)
                # z = y.rereplace(, "")
                
                sig = y[0]
                d = y[1]
                sym = y[2]
                bal = y[3]
                pri = y[4]
                mak = y[5]
                volbs = y[6]
                valbs = y[7]
                fin = y[8]
                g = y[9]
                gp = y[10]
                sav = y[11]
                inter = y[12]

                get = sig+","+d+","+sym+","+bal+","+pri+","+mak+","+volbs+","+valbs+","+fin+","+g+","+gp+","+sav+","+inter
                
                out.append(get)

                signal.append(sig)
                date.append(d)
                symbol.append(sym)
                ratio.append(bal)
                price.append(pri)
                market.append(mak)
                vol.append(volbs)
                val.append(valbs)
                final.append(fin)
                growth.append(g)
                growth_per.append(gp)
                saving.append(sav)
                interest.append(inter)

                break

    # แสดงผลเป็นตาราง
    info = {
        'Signal': signal, 
        'Date': date, 
        'Symbol': symbol,
        'Ratio': ratio,
        'Price': price,
        'Mark': market,
        'Vol': vol,
        'Val': val,
        'Final': final,
        'Growth': growth,
        'Growth_p': growth_per,
        'Saving': saving,
        'Interest': interest
        }    
    print(tabulate(info, headers='keys', tablefmt='fancy_grid'))


    # ส่งออกเป็น txt
    port = open("Portfolio.txt","w")
    for i in range(len(out)):
        tx = out[i]

        port = open("Portfolio.txt","a")
        
        port.write(tx+"\n")
        port.close
    
log()
