import sys
import cv2
import numpy
import time
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from fer import FER
from webcam import VideoThread

def Quit():
    thread.requestInterruption()
    thread.wait()
    App.quit()


App = QtWidgets.QApplication([])
UI = uic.loadUi("QT UI/Presenter_UI.ui")

UI.actionQuit.triggered.connect(Quit)

UI.show()

thread = VideoThread(UI.videoFeed, UI.expressionFeedback)
thread.new_frame_signal.connect(lambda x : thread.Update_Image(x))
thread.start()

sys.exit(App.exec_())
