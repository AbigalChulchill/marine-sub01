from flask import Flask , request
from ROBOT.RB_DY_bot import rebalance_dynamic
from ROBOT.TRACKER_bot import tracker
from ROBOT.STOP_bot import stop
import threading
import variable

app = Flask(__name__)


class GOTO_ROBOT(threading.Thread):
     
    def rb_dinammic(self,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22):
        rebalance_dynamic(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22)

    def robot_track(self,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20):
        tracker(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20)

    def notifi(self,text,token):
        stop(text,token)

@app.route("/<ENTER>/<x>/<y>/<z>/<A1>/<A2>/<A3>/<A4>/<A5>/<A6>/<A7>/<A8>/<A9>/<A10>/<A11>/<A12>/<A13>/<A14>/<A15>/<A16>/<A17>/<A18>/<A19>/<A20>/<A21>/<A22>", methods=['POST'])
def rebalance(ENTER,x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22):
    
    GR = GOTO_ROBOT()
    RM_DYNAMIC = threading.Thread(target=GR.rb_dinammic, args=(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,A21,A22,) , daemon=True)
    BOT_TRACK = threading.Thread(target=GR.robot_track, args=(x,y,z,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14,A15,A16,A17,A18,A19,A20,) , daemon=True)

    if ENTER == "RM_DYNAMIC":
        
        print("(",str(variable.name_domain),")"," ","RM_DYNAMIC")
        RM_DYNAMIC.start()


    elif ENTER == "TRACKER":
        
        print("(",str(variable.name_domain),")"," ","TRACKER")
        BOT_TRACK.start()


    elif ENTER == "ROBOT_STOP":

        text = "ROBOT_STOP"
        print("(",str(variable.name_domain),")"," ",text)
        GR.notifi(text,z)
        

    else :
        text = "STOP by error"
        print("(",str(variable.name_domain),")"," ",text)
        GR.notifi(text,z)
        
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


