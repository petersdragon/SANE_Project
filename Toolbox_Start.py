import sys
import cv2
import numpy
import time
from datetime import timedelta
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTime
from fer import FER
from Webcam import Webcam
from Time_Keeper import Time_Keeper
from Ah_Counter_Server import thread_Ah_Counter, Set_Ah_Indicator
from Generate_Report import Report

def ConvertTime(timeEdit):
    return timeEdit.hour()*3600 + timeEdit.minute()*60 + timeEdit.second()

def Main_Quit():
    thread_webcam.requestInterruption()
    thread_webcam.wait()
    thread_presenting.requestInterruption()
    thread_presenting.wait()
    App.quit()

def Settings_Quit():
    settingsUI.close()

def Report_Quit():
    reportUI.close()

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
    global timerBoundaries
    if not(is_presenting):
        thread_presenting.Start_Timer() # Begin incrementing the speech timer
        thread_Ah_Counter.Reset_Disfluency_Count() # Reset the disfluency count
        
        # Set the timer boundaries to the presenter's settings (even if they were left as the default)
        timerBoundaries["greenIndicator"] = ConvertTime(settingsUI.greenBoundary.time())
        timerBoundaries["yellowIndicator"] = ConvertTime(settingsUI.yellowBoundary.time())
        timerBoundaries["redIndicator"] = ConvertTime(settingsUI.redBoundary.time())

        UI.speechStartStop.setText("⏹️") # Change speech icon during the speech
        is_presenting = True # To ensure that the button will stop the speech timer the next time it is pressed

        # add reset Ah-Counter number here
        # output Ah-counter audio cues

    else: # when done presenting, create report
        disfluencies = {
            "ah" : str(thread_Ah_Counter.Ah_Count),
            "um" : str(thread_Ah_Counter.Um_Count),
            "like" : str(thread_Ah_Counter.Like_Count),
            "so" : str(thread_Ah_Counter.So_Count),
            "long_pause" : str(thread_Ah_Counter.Long_Pause_Count),
            "other" : str(thread_Ah_Counter.Other_Disfluency_Count),
            "total" : str(thread_Ah_Counter.Total_Disfluencies)
        }
        report.Refresh(thread_presenting.Elapsed_Time(), str(timedelta(seconds=ConvertTime(settingsUI.redBoundary.time()))).split('.')[0], disfluencies, settingsUI.presenterNameText.text()) # Create the report in its own window for the presenter to review
        reportUI.show()
        thread_presenting.Reset_Timer() # Reset the presenter timer
        UI.speechStartStop.setText("▶") # Change speech icon after the speech
        is_presenting = False # To ensure that the button will start the speech timer the next time it is pressed

App = QtWidgets.QApplication([])
UI = uic.loadUi("QT_UI/Presenter_UI.ui")
settingsUI = uic.loadUi("QT_UI/Settings_UI.ui") # Set up reference to the settingsUI
reportUI = uic.loadUi("QT_UI/Report_UI.ui") # Set up reference to the reportUI
# Initialize the timer indicator boundaries to the default value
timerBoundaries = {
    "greenIndicator" : ConvertTime(settingsUI.greenBoundary.time()),
    "yellowIndicator" : ConvertTime(settingsUI.yellowBoundary.time()),
    "redIndicator" : ConvertTime(settingsUI.redBoundary.time())
}
report = Report(reportUI)
thread_webcam = Webcam(UI.videoFeed, UI.expressionFeedback, delay=15) # -1 for off, 15 will poll every 15th frame
thread_webcam.new_frame_signal.connect(lambda x : thread_webcam.Update_Image(x))
thread_webcam.start()

is_presenting = False # Boolean to know if the timer needs to be going
thread_presenting = Time_Keeper(UI.elapsedTime, UI.timerIndicator, timerBoundaries) # Define the thread that will time the presenter
thread_presenting.start()

Set_Ah_Indicator(UI.ahIndicator)
thread_Ah_Counter.start()

UI.actionQuit.triggered.connect(Main_Quit)
UI.actionSettings.triggered.connect(Settings_Click)
UI.settingsButton.clicked.connect(Settings_Click)
UI.speechStartStop.clicked.connect(Speech_Click)
UI.show()

settingsUI.actionQuit.triggered.connect(Settings_Quit)
reportUI.actionQuit.triggered.connect(Report_Quit)
reportUI.saveButton.clicked.connect(lambda : report.Save_Report())

sys.exit(App.exec_())
