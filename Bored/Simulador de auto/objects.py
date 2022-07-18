import json
import numpy as np
from scipy.integrate import odeint
from PyQt5.QtCore import QObject, pyqtSignal

class Car(QObject):

    def __init__(self):
        super().__init__()

        self.front = None
        self.back = None
        self.scale = None
        self.ref_L = 0
        self.ref_R = 0
        self.vel_L = 0
        self.vel_R = 0

        # Internal variables
        self.velocity = 0
        self.angular_velocity = 0

        # Wheels torque
        self.motor_L = 0
        self.motor_R = 0

        # PID variables
        self.motor_L_prev = 0
        self.motor_R_prev = 0
        self.error_L = 0
        self.error_R = 0
        self.error_L_prev = 0 
        self.error_R_prev = 0
        self.error_L_pprev = 0
        self.error_R_pprev = 0

        # Other parameters
        self.J = self.p("MASS")/12 * (self.p("CAR_WIDTH")**2 + self.p("CAR_LENGHT")**2)  # Inertia moment [kg*m**2]

    def center_of_rotation(self):
        return self.back*(1 - self.p("gamma_1")) + self.front*self.p("gamma_1")

    def set_speed(self, command):
        if command == "w":
            self.ref_L += 1.0
            self.ref_R += 1.0
        elif command == "a":
            self.ref_L -= 0.2
            self.ref_R += 0.2
        elif command == "s":
            self.ref_L -= 1.0
            self.ref_R -= 1.0
        elif command == "d":
            self.ref_L += 0.2
            self.ref_R -= 0.2
        elif command == "stop":
            self.ref_L = self.ref_R = 0.0
        
    def move(self, time):
        self.PID(time)
        self.update_vel(time)
        step = self.velocity * time
        theta = -self.angular_velocity * time
        
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

    def PID(self, period):
        k0 = self.p("kp")*(1 + self.p("ki")*period + self.p("kd")/period)
        k1 = -self.p("kp")*(1 + 2*self.p("kd")/period)
        k2 = self.p("kp")*self.p("kd")/period

        self.error_L = (self.ref_L - self.vel_L)  # m/s
        self.error_R = (self.ref_R - self.vel_R)  # m/s
        self.motor_L = self.motor_L_prev + k0*self.error_L + k1*self.error_L_prev + k2*self.error_L_pprev  # Nm
        self.motor_R = self.motor_R_prev + k0*self.error_R + k1*self.error_R_prev + k2*self.error_R_pprev  # Nm
        
        # Update PID variables
        self.motor_L_prev = self.motor_L
        self.motor_R_prev = self.motor_R
        self.error_L_pprev = self.error_L_prev
        self.error_R_pprev = self.error_R_prev
        self.error_L_prev = self.error_L
        self.error_R_prev = self.error_R

    def update_vel(self, deltaT):
        # dynamic function for differential traction car
        t = np.linspace(0, deltaT, 2)
        
        def v_fun(v, t):
            dvdt = 1/self.p("MASS") * (self.motor_R/self.p("WHEEL_RADIOUS") + self.motor_L/self.p("WHEEL_RADIOUS") - self.p("LINEAR_FRICTION")*v)
            return dvdt
        self.velocity = odeint(v_fun, self.velocity, t)[-1][0]

        def w_fun(w, t):
            dwdt = 1/self.J * (self.p("CAR_LENGHT")/2 * self.motor_R/self.p("WHEEL_RADIOUS") - self.p("CAR_LENGHT")/2 * self.motor_L/self.p("WHEEL_RADIOUS") - self.p("ANGULAR_FRICTION")*w)
            return dwdt
        self.angular_velocity = odeint(w_fun, self.angular_velocity, t)[-1][0]

        self.vel_L = self.velocity - self.angular_velocity*self.p("CAR_LENGHT")/4
        self.vel_R = self.velocity + self.angular_velocity*self.p("CAR_LENGHT")/4

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

    