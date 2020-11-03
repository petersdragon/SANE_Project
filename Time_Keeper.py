import time
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from datetime import datetime, timedelta
from stopwatch import Stopwatch

class Time_Keeper(QThread):
    def __init__(self, elapsedTime):
        super().__init__()
        self.elapsedTime = elapsedTime
        self.stopwatch = Stopwatch()

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

    def Reset_Timer(self):
        self.stopwatch.stop()
        self.stopwatch.reset()
        self.Update_Timer()

    