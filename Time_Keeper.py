import time

class Time_Keeper():
    def __init__(self):
        self.start_time = None
        self.speech_duration = None

    def Start_Timer(self):
        # begin presentation timer
        self.start_time = time.time()

    def End_Timer(self):
        # get presentation duration
        self.speech_duration = self.Elapsed_Time()

    def Elapsed_Time(self):
        current_time = time.time()
        return current_time - self.start_time


    