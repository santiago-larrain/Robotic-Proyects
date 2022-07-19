import numpy as np
import pygame       # Load pygame for IO-interfacing 
import json
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "Simulador/parameters/display_parameters.json"

class TaskManager(QObject):

    set_speed_signal = pyqtSignal(tuple)
    speed_controller_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
    
    def manage_keyboard(self, key):
        # Check manual drive
        if key == "w":
            self.speed_controller_signal.emit(False)
            self.set_speed_signal.emit((1,1))
        elif key == "a":
            self.speed_controller_signal.emit(False)
            self.set_speed_signal.emit((0.35,0.65))
        elif key == "s":
            self.speed_controller_signal.emit(False)
            self.set_speed_signal.emit((-1,-1))
        elif key == "d":
            self.speed_controller_signal.emit(False)
            self.set_speed_signal.emit((0.65,0.35))
        elif key == "stop":
            self.speed_controller_signal.emit(False)
            self.set_speed_signal.emit((0,0))

        else:
            # Set automatic drive
            self.speed_controller_signal.emit(True)
            
