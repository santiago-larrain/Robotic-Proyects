from threading import Thread
import json
import time
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal

from tasks import task_1, task_2

P_ROUTE = "parameters/controller_parameters.json"

class Controller(QObject):

    update_message_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.motor_speed = (0,0)
        self.task = "0"
        self.thread = None
        self.active = False

    def automatic_tasks(self):
        while self.active:
            start = time.time()
            if self.task == "1":
                self.motor_speed = task_1(self.motor_speed)
                self.update_message_signal.emit(self.motor_speed)
            elif self.task == "2":
                self.motor_speed = task_2(self.motor_speed)
                self.update_message_signal.emit(self.motor_speed)
            
            
            sleep = max(self.p("SLEEP") - (time.time() - start), 0)
            time.sleep(sleep)
    
    def set_manual_drive(self, speed):
        self.task = "M"     # Para indicar que está en control manual
        if self.active:
            self.end()  # Terminar con el controlador automático
        self.motor_speed = speed    # Tuple (m1, m2)
        self.update_message_signal.emit(self.motor_speed)
    
    def set_task(self, task):
        self.task = task
        if not self.active:
            self.restart()

    def p(self, parameter):
        with open(P_ROUTE, "r") as file:
            data = json.load(file)
            try:
                return data[parameter]
            except KeyError:
                print(f"\033[1mWARNING: [Display]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
                return None

    def restart(self):
        self.end()
        self.active = True
        self.thread = Thread(target= self.automatic_tasks, daemon= False)
        self.thread.start()

    def end(self):
        self.active = False
        try:
            self.thread.join()
        except AttributeError:
            pass
        self.thread = None