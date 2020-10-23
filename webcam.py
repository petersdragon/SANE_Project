import sys
import cv2
import numpy
import time
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from fer import FER

class Webcam(QThread):
    new_frame_signal = pyqtSignal(numpy.ndarray)
    
    def __init__(self, videoFeed, emotionFeedback, delay):
        super().__init__()
        self.video_capture_device = cv2.VideoCapture(0)
        self.videoFeed = videoFeed
        self.emotionFeedback = emotionFeedback
        self.detector = FER()
        self.delay_FER_read = 0 
        self.delay = delay # only perform facial recognition once every certain number of frames to improve runtime experience

    def run(self):
        
        # Capture from Webcam
        width = 320
        height = 240
        self.video_capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video_capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        while True:
            if self.isInterruptionRequested():
                self.video_capture_device.release()
                return
            else:
                ret, frame = self.video_capture_device.read()
                if ret:
                    self.new_frame_signal.emit(frame)

    def Update_Image(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        self.videoFeed.setPixmap(QtGui.QPixmap(qImg).scaled(self.videoFeed.width(),self.videoFeed.height(),Qt.KeepAspectRatio))
        if self.delay == -1:
            pass
        elif self.delay_FER_read == self.delay: # only perform facial recognition once every <delay> frames
            emotion, score = self.detector.top_emotion(frame)
            self.emotionFeedback.setText(emotion)
            self.delay_FER_read = 0
        else:
            self.delay_FER_read += 1

