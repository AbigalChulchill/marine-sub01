import requests
import PySimpleGUI as sg



sg.theme('Default')
layout = [
 [sg.Frame('', layout = [
   [sg.T('MARINE INVESMENT by Mr.HD',size=(35,1), key='label')],

   [sg.T(' '*11),sg.B('START TRADING ', key='START', size=(20, 5))],
   [sg.T(' '*11),sg.B('STOP TRADING ', key='STOP', size=(20, 5))],
   [sg.T(' '*11),sg.B('REVIEW ', key='RE', size=(20, 5))],
   [sg.T(' '*11),sg.B('TRACK ', key='TR', size=(20, 5))],
   [sg.T(' '*11),sg.B('EXIT', key='EXIT' , size=(20, 5))],
   [sg.T('My name is harith detbun i am seaman')]
])]]

window = sg.Window('MARINE INVESMENT', layout)

if __name__ == '__main__':

    while True:
        event, values = window.read()
        
        if event == 'START':
            requests.post(url="https://robot-marine.herokuapp.com//START")
            # print("I LOVE")
            # try:
            #     SM_t.start()
            # except:
            #     SM.resume(command=False)
            #     SM.run()
        
        if event == 'STOP':
            requests.post(url="https://robot-marine.herokuapp.com//STOP")
            # print("I FILE")
            # SM.stop()

        if event == 'RE':
            requests.post(url="https://robot-marine.herokuapp.com//REVIEW")

        if event == 'TR':
            requests.post(url="https://robot-marine.herokuapp.com//TRACKER")


        if event == 'EXIT':
            break

        if event == 'WIN_CLOSED':
            break
        else :
            pass
            
                  
    window.close()

    # https://build-system.fman.io/qt-designer-download      สร้าง GUI
    # https://github.com/nngogol/PySimpleGUIDesigner         แปลง GUI ด้านบนให้เป็น code ที่ใช้ใน python ได้
    

    