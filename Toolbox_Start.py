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
    thread_webcam.requestInterruption()
    thread_webcam.wait()
    App.quit()

def Settings_Click():
    def FER_Setting():
        if settingsUI.useFER.checkState():
            thread_webcam.delay = 15
        else:
            thread_webcam.delay = -1
            thread_webcam.emotionFeedback.setText("")

    settingsUI.useFER.stateChanged.connect(FER_Setting)
    settingsUI.show()

def Speech_Click():
    global is_presenting
    if not(is_presenting):
        thread_presenting.Start_Timer()
        is_presenting = True
    # add reset Ah-Counter number here
        # increment timer
        # UI.timerDuration.setText("Hello")
        # read inputs from Ah-counter
        # output Ah-counter visual-audio cues
    else:
        # when done presenting, create report
        speech_time = thread_presenting.Elapsed_Time()
        thread_presenting.Reset_Timer()
        is_presenting = False

App = QtWidgets.QApplication([])
UI = uic.loadUi("QT UI/Presenter_UI.ui")
settingsUI = uic.loadUi("QT UI/Settings_UI.ui") # Set up reference to the settingsUI
is_presenting = False # Boolean to know if the timer needs to be going
time_keeper = Time_Keeper(UI.elapsedTime) # Define the class that will time the presenter

thread_webcam = Webcam(UI.videoFeed, UI.expressionFeedback, delay=15) # -1 for off, 15 polls every 15th frame
thread_webcam.new_frame_signal.connect(lambda x : thread_webcam.Update_Image(x))
thread_webcam.start()

thread_presenting = Time_Keeper(UI.elapsedTime)
thread_presenting.start()



UI.actionQuit.triggered.connect(Quit)
UI.actionSettings.triggered.connect(Settings_Click)
UI.settingsButton.clicked.connect(Settings_Click)
UI.speechStartStop.clicked.connect(Speech_Click)

UI.show()

sys.exit(App.exec_())
