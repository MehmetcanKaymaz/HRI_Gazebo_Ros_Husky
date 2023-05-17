import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from vision import Vision
import cv2
import time


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

        #######################################################3
        self.vision = Vision()
        #self.start()

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


    def start(self):
        current_level = 1
        while True:
            time.sleep(0.5)
            label = self.vision.single_update()
            print(label)
            if label == 3:
                current_level += 1
            elif label == 4:
                current_level -= 1

            current_level = max(1, current_level)
            current_level = min(3, current_level)

            print(current_level)

            if current_level == 1:
                self.checkBox.setChecked(True)
                self.checkBox_2.setChecked(False)
                self.checkBox_3.setChecked(False)
            elif current_level == 2:
                self.checkBox.setChecked(False)
                self.checkBox_2.setChecked(True)
                self.checkBox_3.setChecked(False)
            else:
                self.checkBox.setChecked(False)
                self.checkBox_2.setChecked(False)
                self.checkBox_3.setChecked(True)

            if label == 2:
                break

        print("Done")
        self.vision.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
