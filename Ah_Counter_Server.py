import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread

import flask, os
from flask import render_template, url_for


app = flask.Flask(__name__)
app.config["DEBUG"] = False

disfluencyIndicator = None

def Set_Ah_Indicator(indicator):
    global disfluencyIndicator
    disfluencyIndicator = indicator

class FlaskServer(QThread):
    def __init__(self,app):
        super().__init__()
        self.Ah_Count = 0
        self.Um_Count = 0
        self.Like_Count = 0
        self.So_Count = 0
        self.Long_Pause_Count = 0
        self.Other_Disfluency_Count = 0
        self.app = app

    def run(self):
       self.app.run(host='0.0.0.0')

thread_Ah_Counter = FlaskServer(app)

@app.route('/', methods=['GET'])
def Home():
    return render_template("Ah_Counter.html")

@app.route('/ahCounter', methods=['POST'])
def Ah_Counter():
    thread_Ah_Counter.Ah_Count += int(flask.request.form["count"])
    Disfluency_Feedback()

@app.route('/umCounter', methods=['POST'])
def Um_Counter():
    thread_Ah_Counter.Um_Count += int(flask.request.form["count"])
    Disfluency_Feedback()

@app.route('/likeCounter', methods=['POST'])
def Like_Counter():
    thread_Ah_Counter.Like_Count += int(flask.request.form["count"])
    Disfluency_Feedback()

@app.route('/soCounter', methods=['POST'])
def So_Counter():
    thread_Ah_Counter.So_Count += int(flask.request.form["count"])
    Disfluency_Feedback()

@app.route('/longPauseCounter', methods=['POST'])
def Long_Pause_Counter():
    thread_Ah_Counter.Long_Pause_Count += int(flask.request.form["count"])
    Disfluency_Feedback()

@app.route('/otherDisfluencyCounter', methods=['POST'])
def Other_Disfluency_Counter():
    thread_Ah_Counter.Other_Disfluency_Count += int(flask.request.form["count"])
    Disfluency_Feedback()


def Disfluency_Feedback():
    global disfluencyIndicator
    FG_Color = "rgb(0,0,255);"
    disfluencyIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")
    print("Ah = " + str(thread_Ah_Counter.Ah_Count) + "\n")
    print("Um = " + str(thread_Ah_Counter.Um_Count) + "\n")
    print("Like = " + str(thread_Ah_Counter.Like_Count) + "\n")
    print("So = " + str(thread_Ah_Counter.So_Count) + "\n")
    print("Long Pause = " + str(thread_Ah_Counter.Long_Pause_Count) + "\n")
    print("Other = " + str(thread_Ah_Counter.Other_Disfluency_Count) + "\n")
    thread_Ah_Counter.sleep(3)
    FG_Color = "rgb(0,0,0);"
    disfluencyIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")
