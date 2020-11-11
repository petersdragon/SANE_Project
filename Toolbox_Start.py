import sys
import cv2
import numpy
from datetime import timedelta
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTime
from fer import FER
from Webcam import Webcam
from Time_Keeper import Time_Keeper
from Ah_Counter_Server import thread_Ah_Counter, Set_Ah_Indicator
from Generate_Report import Report
from Toolbox_Data import ToolboxData

# Handle when the main Presenter window is closed
def Main_Quit():
    # Gracefully shut down threads
    thread_webcam.requestInterruption()
    thread_webcam.wait()
    thread_presenting.requestInterruption()
    thread_presenting.wait()
    App.quit()

# Handle when the Settings window is closed
def Settings_Quit():
    settingsUI.close()

# Handle when the Report window is closed
def Report_Quit():
    reportUI.close()

# Handle when the Settings button is clicked
def Settings_Click():
    # Check if the Facial Expression Recognition (FER) setting is true or false, and set the GUI label appropriately
    def FER_Setting():
        # Check if the FER is able to identify a face that it can read
        if settingsUI.useFER.checkState():
            # Only read every fifteenth frame to reduce load on the program
            thread_webcam.delay = 15
        else:
            # if the FER cannot read the expression, display an empty string so that it does not display incorrect data
            thread_webcam.delay = -1
            thread_webcam.emotionFeedback.setText("")
    # Handle when the setting for when the user enables/disables the FER option
    settingsUI.useFER.stateChanged.connect(FER_Setting)
    settingsUI.show()

# Handle when the Start/Stop presenting button is clicked
def Speech_Click():
    # If the button is clicked to start the speech
    if not(data_object.getIsPresenting()):
        # Begin incrementing the speech timer
        thread_presenting.Start_Timer() 
        # Reset the disfluency count
        thread_Ah_Counter.Reset_Disfluency_Count() 
        # Set the timer boundaries to the presenter's settings (even if they were left as the default)
        data_object.refreshIndicators()
        # Change speech icon during the speech
        UI.speechStartStop.setText("⏹️")
        # To ensure that the button will stop the speech timer the next time it is pressed
        data_object.setIsPresenting(True) 

    # If the button is clicked to end the speech
    else: # when done presenting, create report
        # Read the number of disfluencies into the data object
        data_object.refreshDisfluenciesCount()
        # Populate the fields in the report window with the results from the current presentation
        report.Refresh(thread_presenting.Elapsed_Time(), str(timedelta(seconds=data_object.getTimerBoundaries()["red"])).split('.')[0], data_object.getDisfluenciesCount(), settingsUI.presenterNameText.text()) # Create the report in its own window for the presenter to review
        reportUI.show()
        # Reset the presenter timer
        thread_presenting.Reset_Timer() 
        # Change speech icon after the speech
        UI.speechStartStop.setText("▶") 
        # To ensure that the button will start the speech timer the next time it is pressed
        data_object.setIsPresenting(False) 

App = QtWidgets.QApplication([])
# Set up reference to the main presenter GUI window
UI = uic.loadUi("QT_UI/Presenter_UI.ui")
# Set up reference to the settings GUI window
settingsUI = uic.loadUi("QT_UI/Settings_UI.ui") 
# Set up reference to the report GUI window
reportUI = uic.loadUi("QT_UI/Report_UI.ui") 
# Initialize the Report object's handle to the Report GUI window
report = Report(reportUI)
# Initialize the data object
data_object = ToolboxData(settingsUI, thread_Ah_Counter)

thread_webcam = Webcam(UI.videoFeed, UI.expressionFeedback, delay=15) # -1 for off, 15 will poll every 15th frame. Define the thread that will control the webcam and FER, then initialize it with the UI components it needs to know about
thread_webcam.new_frame_signal.connect(lambda x : thread_webcam.Update_Image(x))
thread_webcam.start()

thread_presenting = Time_Keeper(UI.elapsedTime, UI.timerIndicator, data_object.getTimerBoundaries()) # Define the thread that will time the presenter then initialize it with the UI components it needs to know about
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
