import sys
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from fer import FER
from Webcam import Webcam
from Time_Keeper import Time_Keeper

class Settings():
    settingsUI = uic.loadUi("QT UI/Settings_UI.ui") # Set up reference to the settingsUI
    fer_thread = None
    
    def __init__(self,settingsUI,fer_thread):
        self.fer_thread = fer_thread
        self.settingsUI = settingsUI

    def FER_Setting(self):
        if self.settingsUI.useFER.checkState():
            self.fer_thread.delay = 15
        else:
            self.fer_thread.delay = -1
            self.fer_thread.emotionFeedback.setText("")

    settingsUI.useFER.stateChanged.connect(FER_Setting)
    settingsUI.show()