import time

class ToolboxData():
    def __init__(self, settingsUI, ah_counter):
        # Initialize the timer indicator boundaries to the default value
        self.settingsUI = settingsUI
        self.ah_counter = ah_counter
        # Initialize the timer boundaries to the default
        self.timerBoundaries = None
        self.refreshIndicators()
        # Initialize the disfluencies count to 0's
        self.disfluencies_count = None
        self.refreshDisfluenciesCount()
        # Boolean to know if the timer needs to be going
        self.is_presenting = False 

    # Convert the timer from the format in the stopwatch to a float format that can be used in other functions
    def ConvertTime(self, timeEdit):
        return timeEdit.hour()*3600 + timeEdit.minute()*60 + timeEdit.second()

    # Get and store the latest data for the timing boundaries from the Settings GUI
    def refreshIndicators(self):
        self.timerBoundaries = {
            "green" : self.ConvertTime(self.settingsUI.greenBoundary.time()),
            "yellow" : self.ConvertTime(self.settingsUI.yellowBoundary.time()),
            "red" : self.ConvertTime(self.settingsUI.redBoundary.time())
        }

    # Return the dictionary containing the timer boundaries
    def getTimerBoundaries(self):
        return self.timerBoundaries

    # Populate the disfluencies count with 
    def refreshDisfluenciesCount(self):
        self.disfluencies_count = {
            "ah" : str(self.ah_counter.Ah_Count),
            "um" : str(self.ah_counter.Um_Count),
            "like" : str(self.ah_counter.Like_Count),
            "so" : str(self.ah_counter.So_Count),
            "long_pause" : str(self.ah_counter.Long_Pause_Count),
            "other" : str(self.ah_counter.Other_Disfluency_Count),
            "total" : str(self.ah_counter.Total_Disfluencies)
        }

    # Return the dictionary of disfluencies count
    def getDisfluenciesCount(self):
        return self.disfluencies_count

    # Set the flag for determinine whether the presenter is currently presenting or has finished presenting to run the appropriate functions
    def setIsPresenting(self, is_presenting):
        self.is_presenting = is_presenting

    # Return whether the presenter is presenting or has finished presenting to run the appropriate functions
    def getIsPresenting(self):
        return self.is_presenting