import numpy as np
import json
import pygame

from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "parameters/task_manager_parameters.json"

class TaskManager(QObject):

    restart_signal = pyqtSignal()
    end_signal = pyqtSignal()

    manual_drive_signal = pyqtSignal(tuple)
    task_signal = pyqtSignal(str)
    toggle_OnOff_coms_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.task = 0
        
    def manage_keyboard(self, key):
        # Check for start/end program
        if key == pygame.K_ESCAPE:
            self.end_program()
        elif key == pygame.K_RETURN:
            self.restart_program()
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

    def p(self, parameter):
        with open(self.p_route, "r") as file:
            data = json.load(file)
            try:
                return data[parameter]
            except KeyError:
                print(f"\033[1mWARNING: [Task Manager]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
                return None

    def restart_program(self):
        self.restart_signal.emit()

    def end_program(self):
        self.end_signal.emit()
