import json
import numpy as np

class Car:

    def __init__(self):
        self.front = None
        self.back = None
        self.scale = None
        self.motor_L_RPM = 200
        self.motor_R_RPM = 120

    def center_of_rotation(self):
        return self.back*(1 - self.p("gamma_1")) + self.front*self.p("gamma_1")

    def move(self, time):
        velocity = (self.motor_R_RPM + self.motor_L_RPM)/2 *self.p("WHEEL_RADIOUS") /60  # [m/s]
        angular_velocity = (self.motor_R_RPM - self.motor_L_RPM)*self.p("WHEEL_RADIOUS")/(self.p("CAR_WIDTH")/2) /60
        step = velocity * time
        theta = -angular_velocity * time
        
        # Save initial points
        center = self.center_of_rotation()/self.scale
        front = np.array([self.front[0], self.front[1]])/self.scale - center
        back = np.array([self.back[0], self.back[1]])/self.scale - center

        # Move the vehicle
        steps = np.array([step*np.cos(theta + self.angle(front - back, np.array([1,0]))), -step*np.sin(theta + self.angle(front - back, np.array([1,0])))])
        front = front + steps
        back = back + steps
        # Rotate the vehicle
        front = center + self.R(theta).dot(front)
        back = center + self.R(theta).dot(back) 
        
        self.front = self.adjust_array(front)
        self.back = self.adjust_array(back)

    def adjust_array(self, vector):
        return np.array([vector[0]*self.scale, vector[1]*self.scale])

    def R(self, t):
        # Matriz de rotación para un ángulo t en radianes.
        return np.array([[np.cos(t), -np.sin(t)], 
                        [np.sin(t), np.cos(t)]])
    
    def angle(self, v1, v2):
        # Producto punto y cruz
        sin = np.cross(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
        cos = v1.dot(v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
        if sin >= 0 and cos >= 0:
            return np.arcsin(sin)
        elif sin >= 0 and cos < 0:
            return np.pi - np.arccos(-cos)
        elif sin < 0 and cos < 0:
            return np.arccos(-cos) - np.pi
        elif sin < 0 and cos >= 0:
            return np.arcsin(sin)
        return 0
    
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

    