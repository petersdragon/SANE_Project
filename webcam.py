import sys
import cv2
import numpy
import time
from PyQt5 import QtWidgets,QtGui,uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from fer import FER

class VideoThread(QThread):
    new_frame_signal = pyqtSignal(numpy.ndarray)

    def __init__(self, videoLabel, emotionText):
        super().__init__()
        self.video_capture_device = cv2.VideoCapture(0)
        self.videoLabel = videoLabel
        self.emotionText = emotionText
        self.detector = FER()

    def run(self):
        
        # Capture from Webcam
        width = 320
        height = 240
        self.video_capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video_capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        while True:
#            start_time = time.time()
            if self.isInterruptionRequested():
                self.video_capture_device.release()
                return
            else:
                ret, frame = self.video_capture_device.read()
#                if ret:
#                    self.new_frame_signal.emit(frame)
#            UI.fpsLabel.setText(str(int(1.0/(time.time()-start_time)))+" fps")

    def Update_Image(self, frame):
        height, width, channel = frame.shape
        bytesPerLine = 3 * width
        qImg = QtGui.QImage(frame.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        qImg = qImg.rgbSwapped()
        self.videoLabel.setPixmap(QtGui.QPixmap(qImg).scaled(self.videoLabel.width(),self.videoLabel.height(),Qt.KeepAspectRatio))
        emotion, score = self.detector.top_emotion(frame)
        self.emotionText.setText(emotion)

