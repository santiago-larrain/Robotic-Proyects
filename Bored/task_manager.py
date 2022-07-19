import numpy as np
import pygame       # Load pygame for IO-interfacing 
import json
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "Simulador/parameters/display_parameters.json"

class TaskManager(QObject):

    restart_signal = pyqtSignal()
    end_signal = pyqtSignal()

    set_speed_signal = pyqtSignal(tuple)
    speed_controller_signal = pyqtSignal(bool)
    toggle_OnOff_coms_signal = pyqtSignal()
    add_car_signal = pyqtSignal(object)
    set_speed_1_signal = pyqtSignal(tuple)
    set_speed_2_signal = pyqtSignal(tuple)
    change_car_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.cars = []
        self.car_counter = 0
        self.current_car = 0
    
    def manage_keyboard(self, key):
        # Check for start/end program
        if key == pygame.K_RETURN:
            self.start_program()
        elif key == pygame.K_ESCAPE:
            self.end_program()
        else:
            # Check manual drive
            if key == pygame.K_w:
                self.speed_controller_signal.emit(False)
                self.set_speed_signal.emit((1,1))
            elif key == pygame.K_a:
                self.speed_controller_signal.emit(False)
                self.set_speed_signal.emit((0.35,0.65))
            elif key == pygame.K_s:
                self.speed_controller_signal.emit(False)
                self.set_speed_signal.emit((-1,-1))
            elif key == pygame.K_d:
                self.speed_controller_signal.emit(False)
                self.set_speed_signal.emit((0.65,0.35))
            elif key == pygame.K_SPACE:
                self.speed_controller_signal.emit(False)
                self.set_speed_signal.emit((0,0))
            else:
                # Set automatic drive and check other entrys
                self.speed_controller_signal.emit(True)
                if key == pygame.K_o:
                    self.toggle_OnOff_coms_signal.emit()
                elif key == pygame.K_c:
                    try:
                        car = self.cars[self.car_counter]
                        self.add_car_signal.emit(car)
                        self.car_counter += 1
                    except IndexError:
                        print(f"\033[1mWARNING:\033[0m There are no more cars")
                else:
                    print(key)

    def start_program(self):
        self.restart_signal.emit()

    def end_program(self):
        self.end_signal.emit()
