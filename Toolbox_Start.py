import sys
import cv2
import numpy
import time
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from fer import FER
from Webcam import Webcam
from Time_Keeper import Time_Keeper


def Quit():
    thread.requestInterruption()
    thread.wait()
    App.quit()

def Settings_Click():
    def FER_Setting():
        if settingsUI.useFER.checkState():
            thread.delay = 15
        else:
            thread.delay = -1
            thread.emotionFeedback.setText("")

    settingsUI.useFER.stateChanged.connect(FER_Setting)
    settingsUI.show()


App = QtWidgets.QApplication([])
UI = uic.loadUi("QT UI/Presenter_UI.ui")
settingsUI = uic.loadUi("QT UI/Settings_UI.ui") # Set up reference to the settingsUI

thread = Webcam(UI.videoFeed, UI.expressionFeedback, delay=15) # -1 for off, 15 is ideal
thread.new_frame_signal.connect(lambda x : thread.Update_Image(x))
thread.start()

UI.actionQuit.triggered.connect(Quit)
UI.actionSettings.triggered.connect(Settings_Click)
UI.settingsButton.clicked.connect(Settings_Click)

UI.show()


sys.exit(App.exec_())
