import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os
import threading
from run_sim import Sim
import multiprocessing

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 442)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 10, 401, 61))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 170, 221, 61))
        self.label_2.setObjectName("label_2")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(250, 190, 92, 23))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(340, 190, 92, 23))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(440, 190, 92, 23))
        self.checkBox_3.setObjectName("checkBox_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(120, 290, 291, 91))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #######################################################

        self.selected_level=1


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; font-weight:600;\">LIMITLESS AI</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Select Level : </span></p></body></html>"))
        self.checkBox.setText(_translate("MainWindow", "Level 1"))
        self.checkBox_2.setText(_translate("MainWindow", "Level 2"))
        self.checkBox_3.setText(_translate("MainWindow", "Level 3"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

        self.pushButton.clicked.connect(self.start)

        self.checkBox.stateChanged.connect(self.check_box1)
        self.checkBox_2.stateChanged.connect(self.check_box2)
        self.checkBox_3.stateChanged.connect(self.check_box3)


    def check_box1(self, state):
        if state==2:
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.selected_level=1

    def check_box2(self, state):
        if state==2:
            self.checkBox.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.selected_level=2

    def check_box3(self, state):
        if state==2:
            self.checkBox_2.setChecked(False)
            self.checkBox.setChecked(False)
            self.selected_level=3

    def run_game(self):
        if self.selected_level==1:
            os.system("./run_level1.sh")
        elif self.selected_level==2:
            os.system("./run_level2.sh")
        elif self.selected_level==3:
            os.system("./run_level3.sh")

    def start(self):
        print("Starting Game")
        p=multiprocessing.Process(target=self.run_game)
        p.start()

        time.sleep(10)
        
        sim=Sim(level=self.selected_level)
        sim.loop()

        p.kill()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
