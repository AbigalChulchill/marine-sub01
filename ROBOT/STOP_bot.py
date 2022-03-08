from songline import Sendline
import emoji
import sys

def stop(text,token,domain_name):
    
    messenger = Sendline(token)
        
    messenger.sendtext("\n\n"+emoji.emojize(":bangbang:", use_aliases=True)+"("+str(domain_name)+")"+str(text)+emoji.emojize(":bangbang:", use_aliases=True))


    sys.exit()
