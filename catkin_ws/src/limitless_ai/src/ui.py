#!/usr/bin/env python3

import os
import sys
import time
import rospy
import subprocess
from std_msgs.msg import Int32
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1338, 838)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: white")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 30, 681, 131))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_easy = QtWidgets.QLabel(self.centralwidget)
        self.label_easy.setGeometry(QtCore.QRect(30, 210, 400, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_easy.setFont(font)
        self.label_easy.setStyleSheet("background-color: lightgrey")
        self.label_easy.setFrameShape(QtWidgets.QFrame.Box)
        self.label_easy.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_easy.setLineWidth(4)
        self.label_easy.setAlignment(QtCore.Qt.AlignCenter)
        self.label_easy.setObjectName("label_easy")
        self.label_medium = QtWidgets.QLabel(self.centralwidget)
        self.label_medium.setGeometry(QtCore.QRect(450, 210, 400, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_medium.setFont(font)
        self.label_medium.setStyleSheet("background-color: lightgreen")
        self.label_medium.setFrameShape(QtWidgets.QFrame.Box)
        self.label_medium.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_medium.setLineWidth(4)
        self.label_medium.setAlignment(QtCore.Qt.AlignCenter)
        self.label_medium.setObjectName("label_medium")
        self.label_hard = QtWidgets.QLabel(self.centralwidget)
        self.label_hard.setGeometry(QtCore.QRect(870, 210, 400, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_hard.setFont(font)
        self.label_hard.setStyleSheet("background-color: lightgrey")
        self.label_hard.setFrameShape(QtWidgets.QFrame.Box)
        self.label_hard.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_hard.setLineWidth(4)
        self.label_hard.setAlignment(QtCore.Qt.AlignCenter)
        self.label_hard.setObjectName("label_hard")
        self.label_play = QtWidgets.QLabel(self.centralwidget)
        self.label_play.setGeometry(QtCore.QRect(450, 490, 400, 120))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_play.setFont(font)
        self.label_play.setStyleSheet("background-color: white")
        self.label_play.setFrameShape(QtWidgets.QFrame.Box)
        self.label_play.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_play.setLineWidth(4)
        self.label_play.setAlignment(QtCore.Qt.AlignCenter)
        self.label_play.setObjectName("label_play")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(470, 630, 371, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(880, 410, 500, 500))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("resources/husky.webp"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        self.label_7.raise_()
        self.label.raise_()
        self.label_easy.raise_()
        self.label_medium.raise_()
        self.label_hard.raise_()
        self.label_play.raise_()
        self.label_6.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.label_6.hide()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Limitless AI Game"))
        self.label.setText(_translate("MainWindow", "Limitless AI Game"))
        self.label_easy.setText(_translate("MainWindow", "EASY"))
        self.label_medium.setText(_translate("MainWindow", "MEDIUM"))
        self.label_hard.setText(_translate("MainWindow", "HARD"))
        self.label_play.setText(_translate("MainWindow", "PLAY"))
        self.label_6.setText(_translate("MainWindow", "Starting game ..."))


def start_game():
    global launch_mod
    if launch_mod == 1:
        subprocess.run("./run_level1.sh", shell=True)
    elif launch_mod == 2:
        subprocess.run("./run_level2.sh", shell=True)
    elif launch_mod == 3:
        subprocess.run("./run_level3.sh", shell=True)
    else:
        return

    subprocess.run("rosnode kill /vision_system", shell=True)
    time.sleep(1)
    os.system(f"rosparam set __level {launch_mod}")
    os.system("rosrun limitless_ai run_sim.py &")
    QCoreApplication.exit(0)


# UI Ayarlari
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
tahmin = 0
launch_mod = 2

def callback(data):
    global tahmin    
    global launch_mod
    tahmin = data.data
    print("Tahmin:", tahmin)

    if tahmin == 3: # Go Left
        if launch_mod == 2:
            ui.label_medium.setStyleSheet("background-color:lightgrey")
            ui.label_easy.setStyleSheet("background-color:lightgreen")
            launch_mod = 1
        elif launch_mod == 3:
            ui.label_hard.setStyleSheet("background-color:lightgrey")
            ui.label_medium.setStyleSheet("background-color:lightgreen")
            launch_mod = 2
    elif tahmin == 4:
        if launch_mod == 2:
            ui.label_medium.setStyleSheet("background-color:lightgrey")
            ui.label_hard.setStyleSheet("background-color:lightgreen")
            launch_mod = 3
        elif launch_mod == 1:
            ui.label_easy.setStyleSheet("background-color:lightgrey")
            ui.label_medium.setStyleSheet("background-color:lightgreen")
            launch_mod = 2
    elif tahmin == 2:
        ui.label_play.setStyleSheet("background-color:lightblue")
        ui.label_6.show()
        time.sleep(3)
        start_game()
        time.sleep(10)

def start_ui_system():
    # ROS Ayarlari
    rospy.init_node('ui_system', anonymous=True)
    rospy.Subscriber("tahminler", Int32, callback)

    MainWindow.show()

    #rospy.spin()
    sys.exit(app.exec_())

start_ui_system()
