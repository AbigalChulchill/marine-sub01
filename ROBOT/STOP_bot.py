from songline import Sendline
import emoji
import sys
import variable

def stop(text,token):
    
    messenger = Sendline(token)
        
    messenger.sendtext("\n\n"+emoji.emojize(":bangbang:", use_aliases=True)+"("+str(variable.name_domain)+")"+" "+str(text)+emoji.emojize(":bangbang:", use_aliases=True))

    sys.exit()
