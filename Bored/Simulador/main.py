import sys
from PyQt5.QtWidgets import QApplication
from display import Display
from objects import Car, Ball, Arc
import numpy as np

if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])

    display = Display(app)
    display.thread.start()
    robot = Car()
    # Initial points
    robot.back = np.array([display.p("WINDOW_WIDTH")//2 - 10, display.p("WINDOW_LENGHT")//2])
    robot.front = np.array([display.p("WINDOW_WIDTH")//2 + 10, display.p("WINDOW_LENGHT")//2])
    robot.scale = display.p("SCALE")
    display.cars.append(robot)

    # Connections
    display.keyboard_signal.connect(
        robot.set_speed
    )

    app.exec_()