def app(): 
    from flask import Flask , request
    import time
    from ROBOT_set import data_dinamic,rev
    from ROBOT_TRACKER_set import tracker
    from RB_DY_bot import rebalance_dynamic
    import threading
    import sys

    # try:
    #     from config import *
    # except:
    #     from config_prod import *

    app = Flask(__name__)


    class SIGNALS_MORNITORING(threading.Thread):
        
        def rb_dinammic(self,begin_money,status,asset_RB,low_gap,zone_1,mid_gap,zone_2,high_gap,zone_3,zone_4,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts):
            rebalance_dynamic(begin_money,status,asset_RB,low_gap,zone_1,mid_gap,zone_2,high_gap,zone_3,zone_4,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts)

        def setting_show(self):
            rev()

        def robot_track(self):
            tracker()

        def job(self):
            data_dinamic()
    
        def run(self):
            self.job()

    SM = SIGNALS_MORNITORING()

    @app.route("/<ENTER>", methods=['POST'])
    def simple(ENTER):
        SM_t = threading.Thread(target=SM.run,daemon=True)
        if ENTER=="START":

            try:
                print("START ROBOT")
                SM_t.start()
            except:
                print("Please click START_again")
                sys.exit()
        elif ENTER=='REVIEW':
            print("REVIEW")
            SM.setting_show()
        else:
            print("STOP ROBOT")
            sys.exit()  
        return "ok"

    @app.route("/<ENTER>/<begin_money>/<status>/<asset_RB>/<low_gap>/<zone_1>/<mid_gap>/<zone_2>/<high_gap>/<zone_3>/<zone_4>/<limit_percent>/<EMAx>/<emat>/<sav>/<asset_saving>/<savx>/<savy>/<line>/<td>/<th>/<tm>/<ts>", methods=['POST'])
    def rebalance(ENTER,begin_money,status,asset_RB,low_gap,zone_1,mid_gap,zone_2,high_gap,zone_3,zone_4,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts):
        RM_DYNAMIC = threading.Thread(target=SM.rb_dinammic, args=(begin_money,status,asset_RB,low_gap,zone_1,mid_gap,zone_2,high_gap,zone_3,zone_4,limit_percent,EMAx,emat,sav,asset_saving,savx,savy,line,td,th,tm,ts,),daemon=True)

        if ENTER == "RM_DYNAMIC":
            print("RM_DYNAMIC")
            RM_DYNAMIC.start()
        else :
            print("something error")

        return "ok"
 
    @app.route("/<ENTER>", methods=['POST'])
    def tracker(ENTER):
        TRACKER = threading.Thread(target=SM.robot_track,daemon=True)

        if ENTER=='TRACKER':
            print("TRACKER")
            TRACKER.start()

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
            
            return "This is buying signals"

        else:
            return "กรุณานำ Link ไปใส่ไว้ที่ Webhook Tradingview"


