

def Quit():
    thread.requestInterruption()
    thread.wait()
    App.quit()


App = QtWidgets.QApplication([])
UI = uic.loadUi("Presenter_UI.ui")

UI.actionQuit.triggered.connect(Quit)

UI.show()

thread = VideoThread()
thread.new_frame_signal.connect(lambda x : thread.Update_Image(x))
thread.start()

sys.exit(App.exec_())
