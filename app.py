from flask import Flask , request
from ROBOT.BALANCE_bot import total_spot , total_sym , saving_sym
from ROBOT.RB_DY_bot import rebalance_dynamic
from ROBOT.RB_FIX_bot import rebalance_fix
from ROBOT.TRACKER_bot import tracker
from ROBOT.STOP_bot import stop

import threading
import setting

app = Flask(__name__)


class GOTO_ROBOT(threading.Thread):
     
    def t_spot(self,x,y,z,dm):
        total_spot(x,y,z,dm)

    def t_sym(self,x,y,z,A1,dm):
        total_sym(x,y,z,A1,dm)

    def sav_sym(self,x,y,z,A1,dm):
        saving_sym(x,y,z,A1,dm)



    def rb_fix(self,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,dm):
        rebalance_fix(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,dm)

    def rb_dinammic(self,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,dm):
        rebalance_dynamic(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,dm)

    def robot_track(self,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,dm):
        tracker(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,dm)

    def notify(self,text,token,dm):
        stop(text,token,dm)

@app.route("/<ENTER>/<x>/<y>/<z>/<A1>/<A2>/<A3>/<A4>/<A5>/<A6>/<A7>/<A8>/<A9>/<A10>/<A11>/<A12>/<A13>/<A14>/<A15>/<A16>/<A17>/<A18>/<A19>/<A20>/<A21>/<A22>", methods=['POST'])
def rebalance(ENTER,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22):
    
    dm = setting.domain_name
    GR = GOTO_ROBOT()
    RB_DYNAMIC = threading.Thread(target=GR.rb_dinammic, args=(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,dm,) , daemon=True)
    RB_FIX = threading.Thread(target=GR.rb_fix, args=(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,dm,) , daemon=True)
    BOT_TRACK = threading.Thread(target=GR.robot_track, args=(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,dm,) , daemon=True)
    
    #---------------------------------------------------------------------------------------------
    if ENTER == "T_SPOT":

        text = "T_SPOT"
        print("(",str(setting.domain_name),")"," ",text)
        GR.t_spot(x,y,z,dm)

    elif ENTER == "T_SYM":

        text = "T_SYM"
        print("(",str(setting.domain_name),")"," ",text)
        GR.t_sym(x,y,z,A1,dm)

    elif ENTER == "S_SYM":

        text = "S_SYM"
        print("(",str(setting.domain_name),")"," ",text)
        GR.sav_sym(x,y,z,A1,dm)
    
    #---------------------------------------------------------------------------------------------

    elif ENTER == "RB_FIX":
        
        print("(",str(setting.domain_name),")"," ","RB_FIX")
        RB_FIX.start()

    elif ENTER == "RB_DYNAMIC":
        
        print("(",str(setting.domain_name),")"," ","RM_DYNAMIC")
        RB_DYNAMIC.start()

    elif ENTER == "TRACKER":
        
        print("(",str(setting.domain_name),")"," ","TRACKER")
        BOT_TRACK.start()

    
    #---------------------------------------------------------------------------------------------

    elif ENTER == "ROBOT_STOP":

        text = "ROBOT_STOP"
        print("(",str(setting.domain_name),")"," ",text)
        GR.notify(text,z,dm)
        
    else :
        text = "STOP by error"
        print("(",str(setting.domain_name),")"," ",text)
        GR.notify(text,z,dm)
        
    return "ok"






@app.route("/", methods=['GET','POST'])
def test_signals():
    
    if request.method == "POST":
        msg = request.data.decode("utf-8")

        """
        PYBOTT : EASY EMA: order
        {{strategy.order.action}}
        @ {{strategy.order.contracts}}
        filled on {{ticker}}.
        New strategy position is
        {{strategy.position_size}}
        """
        #สรุปว่า BTCUSDT ขาย
        #if symbol , signals
            #PlaceSELL
        #else
            #PlaceBUY
        
        return "i'm Yam"

    else:
        return "This is ROBOT MAIN"


