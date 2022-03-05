from songline import Sendline
import emoji
import sys

def stop(token,text):
    
    messenger = Sendline(token)
        
    messenger.sendtext("\n\n"+emoji.emojize(":bangbang:", use_aliases=True)+str(text)+emoji.emojize(":bangbang:", use_aliases=True))

    sys.exit()
