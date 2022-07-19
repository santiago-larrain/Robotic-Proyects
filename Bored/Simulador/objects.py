import json
import numpy as np
import time
from scipy.integrate import odeint
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread


P_ROUTE = "Simulador/parameters/robot_parameters.json"

class Car(QObject):

    position_signal = pyqtSignal(tuple)

    def __init__(self, back, front, scale):
        super().__init__()
        self.thread = None
        self.active = False
        self.initial_back = back
        self.initial_front = front
        self.scale = scale

        self.front = front
        self.back = back
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

    def move(self):
        while self.active:
            start = time.time()
            self.PID()
            self.update_vel()
            step = self.velocity * self.p("PERIOD")
            theta = -self.angular_velocity * self.p("PERIOD")
            
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

            self.position_signal.emit((self.back, self.front))

            sleep = max(self.p("PERIOD") - (time.time() - start), 0)
            time.sleep(sleep)

        print("\033[1mMESSAGE:\033[0m Car terminated")

    def center_of_rotation(self):
        return self.back*(1 - self.p("gamma_1")) + self.front*self.p("gamma_1")

    def set_speed(self, command):
        self.ref_L, self.ref_R = command[0], command[1]

    def PID(self):
        k0 = self.p("kp")*(1 + self.p("ki")*self.p("PERIOD") + self.p("kd")/self.p("PERIOD"))
        k1 = -self.p("kp")*(1 + 2*self.p("kd")/self.p("PERIOD"))
        k2 = self.p("kp")*self.p("kd")/self.p("PERIOD")

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

    def update_vel(self):
        # dynamic function for differential traction car
        t = np.linspace(0, self.p("PERIOD"), 2)
        
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
        with open(P_ROUTE, "r") as file:
            data = json.load(file)
            try:
                return data[parameter]
            except KeyError:
                print(f"\033[1mWARNING: [Car]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
                return None

    def restart(self):
        self.end()

        self.active = True
        self.thread = Thread(target= self.move, daemon= False)
        self.thread.start()

    def end(self):
        self.active = False

        self.back = self.initial_back
        self.front = self.initial_front
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

        try:
            self.thread.join()
        except AttributeError:
            pass
        self.thread = None


class Ball:

    def __init__(self):
        pass


class Arc:

    def __init__(self):
        pass

    