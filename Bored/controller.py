import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

class Controller(QObject):

    update_message_signal = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.control_speed = True
        self.thread = threading.Thread(target= self.start, daemon= False)

    def start(self):
        start = time.time()
        while time.time() - start <= 2:
            if self.control_speed:
                self.update_message_signal.emit((1,1))
            time.sleep(0.1)
        self.update_message_signal.emit((0,0))
    
    def toggle_controller(self, control):
        self.control_speed = control # bool
