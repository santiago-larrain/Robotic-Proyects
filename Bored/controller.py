from threading import Thread
import time
import numpy as np

from PyQt5.QtCore import QObject, pyqtSignal

class Controller(QObject):

    update_message_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.control_speed = True
        self.thread = None
        self.active = False

    def start(self):
        start = time.time()
        while time.time() - start <= 9.8 and self.active:
            if self.control_speed:
                if time.time() - start <= 1:
                    self.update_message_signal.emit((1,1))
                elif time.time() - start <= 3:
                    self.update_message_signal.emit((0.35,0.65))
                elif time.time() - start <= 5:
                    self.update_message_signal.emit((0.65,0.35))
                elif time.time() - start <= 6:
                    self.update_message_signal.emit((-2,-2))
                elif time.time() - start <= 7:
                    self.update_message_signal.emit((5,5))
                elif time.time() - start <= 8:
                    self.update_message_signal.emit((-1,-1))
                elif time.time() - start <= 9:
                    self.update_message_signal.emit((-1.1,-1))
                else:
                    self.update_message_signal.emit((-0.9,-1))
            time.sleep(0.1)
        if self.control_speed:
            self.update_message_signal.emit((0,0))
        print("\033[1mMESSAGE:\033[0m Controller terminated")
    
    def toggle_controller(self, control):
        self.control_speed = control # bool

    def restart(self):
        self.end()

        self.active = True
        self.thread = Thread(target= self.start, daemon= False)
        self.thread.start()

    def end(self):
        self.active = False
        try:
            self.thread.join()
        except AttributeError:
            pass
        self.thread = None
