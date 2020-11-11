
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QTime
from datetime import datetime
import webbrowser

class Report():
    def __init__(self, report_UI):
        # Setup window UI and variables
        self.report_UI = report_UI
        self.speech_duration = None
        self.max_speech_duration = None
        self.presenter_name = None
        self.disfluencies = None

    def Refresh(self, speech_duration, max_speech_duration, disfluencies, presenter_name):
        self.speech_duration = speech_duration
        self.max_speech_duration = max_speech_duration
        self.presenter_name = presenter_name
        self.disfluencies = disfluencies
        self.speech_date = datetime.strftime(datetime.today(),"%d-%m-%Y")
        
        # Set widget values from variables
        self.report_UI.presenterName.setText(self.presenter_name)
        self.report_UI.maxSpeechDurationTime.setText(self.max_speech_duration)
        self.report_UI.speechDurationTime.setText(self.speech_duration)
        self.report_UI.ahCount.setText(self.disfluencies["ah"])
        self.report_UI.umCount.setText(self.disfluencies["um"])
        self.report_UI.likeCount.setText(self.disfluencies["like"])
        self.report_UI.soCount.setText(self.disfluencies["so"])
        self.report_UI.longPauseCount.setText(self.disfluencies["long_pause"])
        self.report_UI.otherDisfluencyCount.setText(self.disfluencies["other"])
        self.report_UI.totalDisfluenciesCount.setText(self.disfluencies["total"])
        
    def Save_Report(self):
        file_name = self.presenter_name + "_" + self.speech_date + ".txt"
        report_file = open("Generated_Reports/" + file_name, "w")
        report_string = ""
        report_string += "Presenter Name: \t" + self.presenter_name + "\n"
        report_string += "Date: \t" + self.speech_date + "\n"
        report_string += "Max Speech Duration: \t" + self.max_speech_duration + "\n"
        report_string += "Speech Duration: \t" + self.speech_duration + "\n"
        report_string += "Disfluencies:\n"
        report_string += "\tAh:\t\t" + self.disfluencies["ah"] + "\n"
        report_string += "\tUm:\t\t" + self.disfluencies["um"] + "\n"
        report_string += "\tLike:\t\t" + self.disfluencies["like"] + "\n"
        report_string += "\tSo:\t\t" + self.disfluencies["so"] + "\n"
        report_string += "\tLong Pause:\t" + self.disfluencies["long_pause"] + "\n"
        report_string += "\tOther:\t\t" + self.disfluencies["other"] + "\n"
        report_string += "\tTotal:\t\t" + self.disfluencies["total"] + "\n"
        report_file.write(report_string)
        report_file.close()
        webbrowser.open("Generated_Reports/" + file_name)

