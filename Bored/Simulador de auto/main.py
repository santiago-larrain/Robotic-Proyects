from display import Display
from objects import Car, Ball, Arc
import numpy as np

if __name__ == "__main__":
    display = Display()
    display.thread.start()
    robot = Car()
    robot.back = np.array([550,300])
    robot.front = np.array([650,300])
    display.cars.append(robot)