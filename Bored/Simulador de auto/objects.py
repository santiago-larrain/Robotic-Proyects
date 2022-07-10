import json
import numpy as np

class Car:

    def __init__(self):
        self.front = None
        self.back = None
        self.motor_L_RPM = 0
        self.motor_R_RPM = 0

    def move(self, time):
        velocity = (self.motor_R_RPM - self.motor_L_RPM)*self.p("WHEEL_RADIOUS")
        theta = velocity/(self.p("CAR_WIDTH")/2) * time
        rotated_front = self.R(theta).dot(self.front - self.center_of_rotation())
        rotated_back = self.R(theta).dot(self.back - self.center_of_rotation())

        
    
    def center_of_rotation(self):
        return self.back*(1 - self.p("gamma_1")) + self.front*self.p("gamma_1")

    def R(self, t):
        # Matriz de rotación para un ángulo t en radianes.
        return np.array([[np.cos(t), -np.sin(t)], 
                        [np.sin(t), np.cos(t)]])

    def p(self, parameter):
        with open("robot_parameters.json", "r") as file:
            data = json.load(file)
            try:
                return data[parameter]
            except KeyError:
                print(f"\033[1mWARNING:\033[0m There is no parameter called \033[1m{parameter}\033[0m")
                return None

class Ball:

    def __init__(self):
        pass

class Arc:

    def __init__(self):
        pass

    