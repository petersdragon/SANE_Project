import sys
import random
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QThread

import flask

class FlaskServer(QThread):
    app = flask.Flask(__name__)
    app.config["DEBUG"] = False

    def run(self):
       self.app.run(host='0.0.0.0')

    @app.route('/', methods=['GET'])
    def Home():
        file_str = ""
        with open("./Ah_Counter.html", "r") as file:
            file_str = file.read()
        return file_str
