#!/usr/bin/env python3

import os
import sys
import time
import rospy
import subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from std_msgs.msg import Int32
#from run_sim import Sim

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")

        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 801, 601))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer, 6, 2, 1, 1)
        self.pushButtonPlay = QPushButton(self.gridLayoutWidget)
        self.pushButtonPlay.setObjectName(u"pushButtonPlay")
        self.gridLayout.addWidget(self.pushButtonPlay, 8, 4, 1, 1)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_2, 6, 5, 1, 1)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_4, 6, 0, 1, 1)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer_3, 7, 4, 1, 1)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer_2, 2, 4, 1, 1)
        self.radioButtonHard = QRadioButton(self.gridLayoutWidget)
        self.radioButtonHard.setObjectName(u"radioButtonHard")
        self.gridLayout.addWidget(self.radioButtonHard, 6, 6, 1, 1)
        self.radioButtonMedium = QRadioButton(self.gridLayoutWidget)
        self.radioButtonMedium.setObjectName(u"radioButtonMedium")
        self.radioButtonMedium.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout.addWidget(self.radioButtonMedium, 6, 4, 1, 1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.verticalSpacer, 4, 4, 1, 1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.horizontalSpacer_3, 6, 7, 1, 1)
        self.radioButtonEasy = QRadioButton(self.gridLayoutWidget)
        self.radioButtonEasy.setObjectName(u"radioButtonEasy")
        self.gridLayout.addWidget(self.radioButtonEasy, 6, 1, 1, 1)
        self.labelGameName = QLabel(self.gridLayoutWidget)
        self.labelGameName.setObjectName(u"labelGameName")
        self.gridLayout.addWidget(self.labelGameName, 1, 4, 1, 1)
        self.labelGameModes = QLabel(self.gridLayoutWidget)
        self.labelGameModes.setObjectName(u"labelGameModes")
        self.labelGameModes.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.labelGameModes, 3, 4, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Limitless AI Game", None))
        self.pushButtonPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.radioButtonHard.setText(QCoreApplication.translate("MainWindow", u"Hard", None))
        self.radioButtonMedium.setText(QCoreApplication.translate("MainWindow", u"Medium", None))
        self.radioButtonEasy.setText(QCoreApplication.translate("MainWindow", u"Easy", None))
        self.labelGameName.setText(QCoreApplication.translate("MainWindow", u"Limitless AI Game", None))
        self.labelGameModes.setText(QCoreApplication.translate("MainWindow", u"Game Modes", None))



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
    time.sleep(10)

    os.system("rosrun limitless_ai run_sim.py")
    sys.exit(0)


# UI Ayarlari
app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.radioButtonMedium.setChecked(True)
tahmin = 0
launch_mod = 2

def callback(data):
    global tahmin    
    global launch_mod
    tahmin = data.data
    print("Tahmin:", tahmin)

    if tahmin == 3:
        if ui.radioButtonMedium.isChecked():
            ui.radioButtonEasy.setChecked(True)
            launch_mod = 1
        elif ui.radioButtonHard.isChecked():
            ui.radioButtonMedium.setChecked(True)
            launch_mod = 2
    elif tahmin == 4:
        if ui.radioButtonMedium.isChecked():
            ui.radioButtonHard.setChecked(True)
            launch_mod = 3
        elif ui.radioButtonEasy.isChecked():
            ui.radioButtonMedium.setChecked(True)
            launch_mod = 2
    elif tahmin == 2:
        start_game()

def start_ui_system():
    # ROS Ayarlari
    rospy.init_node('ui_system', anonymous=True)
    rospy.Subscriber("tahminler", Int32, callback)

    MainWindow.show()

    #rospy.spin()
    sys.exit(app.exec_())

start_ui_system()
