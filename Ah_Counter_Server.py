import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread

import flask


app = flask.Flask(__name__)
app.config["DEBUG"] = False

ahIndicator = None

def Set_Ah_Indicator(indicator):
    global ahIndicator
    ahIndicator = indicator

class FlaskServer(QThread):
    def __init__(self,app):
        super().__init__()
        self.Ah_Count = 0
        self.app = app

    def run(self):
       self.app.run(host='0.0.0.0')

thread_Ah_Counter = FlaskServer(app)

@app.route('/', methods=['GET'])
def Home():
    file_str = ""
    with open("./Ah_Counter.html", "r") as file:
        file_str = file.read()
    return file_str

@app.route('/incrementCounter', methods=['POST'])
def Increment_Counter():
    global ahIndicator
    thread_Ah_Counter.Ah_Count += int(flask.request.form["ahCount"])
    FG_Color = "rgb(0,0,255);"
    ahIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")
    thread_Ah_Counter.sleep(3)
    FG_Color = "rgb(0,0,0);"
    ahIndicator.setStyleSheet("QLabel {color : " + FG_Color + "}")
