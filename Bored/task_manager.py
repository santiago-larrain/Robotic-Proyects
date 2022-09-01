import numpy as np
import pygame       # Load pygame for IO-interfacing 
import json
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

class TaskManager(QObject):

    p_route = "Simulador/parameters/display_parameters.json"

    restart_signal = pyqtSignal()
    end_signal = pyqtSignal()

    manual_drive_signal = pyqtSignal(tuple)
    task_signal = pyqtSignal(str)
    toggle_OnOff_coms_signal = pyqtSignal()
    add_car_signal = pyqtSignal(object)
    set_speed_1_signal = pyqtSignal(tuple)
    set_speed_2_signal = pyqtSignal(tuple)
    change_car_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.task = 0
    
    def manage_keyboard(self, key):
        # Check for start/end program
        if key == pygame.K_RETURN:
            self.start_program()
        elif key == pygame.K_ESCAPE:
            self.end_program()
        else:
            # Manual drive
            if key == pygame.K_w:
                self.task = 0
                self.manual_drive_signal.emit((1,1))
            elif key == pygame.K_a:
                self.task = 0
                self.manual_drive_signal.emit((0.35,0.65))
            elif key == pygame.K_s:
                self.task = 0
                self.manual_drive_signal.emit((-1,-1))
            elif key == pygame.K_d:
                self.task = 0
                self.manual_drive_signal.emit((0.65,0.35))
            elif key == pygame.K_SPACE:
                self.task = 0
                self.manual_drive_signal.emit((0,0))
            else:
                if key == pygame.K_o:
                    self.toggle_OnOff_coms_signal.emit()
                if key == pygame.K_0:
                    self.task_signal.emit("0")
                # Automatic drive based on tasks
                else:
                    print(key)

    def start_program(self):
        self.restart_signal.emit()

    def end_program(self):
        self.end_signal.emit()
