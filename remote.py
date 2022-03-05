from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import PySimpleGUI as sg
from app import SM, SM_t
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 600)
        MainWindow.setMinimumSize(QtCore.QSize(400, 600))
        MainWindow.setMaximumSize(QtCore.QSize(400, 600))
        MainWindow.setStyleSheet("background :rgb(31, 51, 76);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 30, 397, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.run = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.run.setFont(font)
        self.run.setStyleSheet("background:rgb(37, 179, 32)")
        self.run.setObjectName("run")
        self.verticalLayout.addWidget(self.run)
        self.stop = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.stop.setFont(font)
        self.stop.setStyleSheet("background:rgb(184, 54, 37)")
        self.stop.setObjectName("stop")
        self.verticalLayout.addWidget(self.stop)
        self.exit = QtWidgets.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(100, 520, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.exit.setFont(font)
        self.exit.setStyleSheet("background-color: rgb(198, 214, 51);")
        self.exit.setObjectName("exit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.run.clicked.connect(self.run_bot)
        self.stop.clicked.connect(self.stop_bot)
        self.exit.clicked.connect(self.exit_remote)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "REMOTE ROBOT"))
        self.run.setText(_translate("MainWindow", "ROBOT RUN"))
        self.stop.setText(_translate("MainWindow", "ROBOT STOP"))
        self.exit.setText(_translate("MainWindow", "EXIT REMOTE"))

    def run_bot(self):
        print("ROBOT RUNNING")
        requests.post(url="https://robot-marine.herokuapp.com//START")

    def stop_bot(self):
        print("ROBOT STOP")
        requests.post(url="https://robot-marine.herokuapp.com//STOP")

    # มีการเพิ่มปุ่ม REVIEW เพื่อแสดงใน ipad แต่ไม่ได้เพิ่มในนี้

    def exit_remote(self):
        print("EXIT REMOTE")
        sys.exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
