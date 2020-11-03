import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from datetime import datetime, timedelta
from stopwatch import Stopwatch

class Time_Keeper(QThread):
    def __init__(self, elapsedTime, timerIndicator, indicatorBoundaries):
        super().__init__()
        self.elapsedTime = elapsedTime
        self.timerIndicator = timerIndicator
        self.stopwatch = Stopwatch()
        self.indicatorBoundaries = indicatorBoundaries

    def run(self):
        self.stopwatch.stop()
        while True:
            self.Update_Timer()
            time.sleep(1)

    def Start_Timer(self):
        # begin presentation timer
        self.stopwatch.reset()
        self.stopwatch.start()

    def Elapsed_Time(self):
        return str(timedelta(seconds=self.stopwatch.duration)).split('.')[0]

    def Update_Timer(self):
        self.elapsedTime.setText(self.Elapsed_Time())
        # For changing the color of the indicator
        if (self.stopwatch.duration >= self.indicatorBoundaries["redIndicator"]):
            FG_Color = "rgb(255,0,0);"
        elif (self.stopwatch.duration >= self.indicatorBoundaries["yellowIndicator"]):
            FG_Color = "rgb(255,255,0);"
        elif (self.stopwatch.duration >= self.indicatorBoundaries["greenIndicator"]):
            FG_Color = "rgb(0,255,0);"
        else:
            FG_Color = "rgb(0,0,0);"

        self.timerIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")

    def Reset_Timer(self):
        self.stopwatch.stop()
        self.stopwatch.reset()
        self.Update_Timer()

    