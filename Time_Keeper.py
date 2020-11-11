import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from datetime import datetime, timedelta
from stopwatch import Stopwatch
from Toolbox_Data import ToolboxData

class Time_Keeper(QThread):
    def __init__(self, elapsedTime, timerIndicator, timerBoundaries):
        super().__init__()
        self.timerBoundaries = timerBoundaries
        self.elapsedTime = elapsedTime
        self.timerIndicator = timerIndicator
        self.stopwatch = Stopwatch()

    # Start running the thread
    def run(self):
        self.Reset_Timer()
        while True:
            self.Update_Timer()
            time.sleep(1)

    # Begin presentation timer
    def Start_Timer(self):
        self.stopwatch.reset()
        self.stopwatch.start()

    # Return the time that the presenter has been presenting in string literal form
    def Elapsed_Time(self):
        return str(timedelta(seconds=self.stopwatch.duration)).split('.')[0]

    # Display the elapsed time and check/update the timer cue on the GUI
    def Update_Timer(self):
        self.elapsedTime.setText(self.Elapsed_Time())
        # For changing the color of the indicator
        if (self.stopwatch.duration >= self.timerBoundaries["red"]):
            FG_Color = "rgb(255,0,0);"
        elif (self.stopwatch.duration >= self.timerBoundaries["yellow"]):
            FG_Color = "rgb(255,255,0);"
        elif (self.stopwatch.duration >= self.timerBoundaries["green"]):
            FG_Color = "rgb(0,255,0);"
        else:
            FG_Color = "rgb(0,0,0);"
        # Set the color determined above on the timing cue
        self.timerIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")

    # Restart the presenter stopwatch
    def Reset_Timer(self):
        self.stopwatch.stop()
        self.stopwatch.reset()
        self.Update_Timer()
    