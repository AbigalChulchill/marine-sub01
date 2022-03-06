from songline import Sendline
import emoji
import sys

def stop(text,token):
    
    messenger = Sendline(token)
        
    messenger.sendtext("\n\n"+emoji.emojize(":bangbang:", use_aliases=True)+str(text)+emoji.emojize(":bangbang:", use_aliases=True))

    sys.exit()
