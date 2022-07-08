from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np


def R(t):
    # Matriz de rotación para un ángulo t en radianes.
    return np.array([[np.cos(t), -np.sin(t)], 
                     [np.sin(t), np.cos(t)]])

# ---------- 2.a ----------
def avanzar(vel_ang, deltaT):
    # Esta función devuelve coordenadas localmente
    vel_tan = vel_ang * r
    # Un giro posititvo será hacia la izquierda y uno negativo hacia la derecha
    theta = (vel_tan[0] - vel_tan[1]) / W * deltaT
    pos_D = np.array([0, -W/2])
    new_pos_D_aux = np.array([vel_tan[0] * deltaT, -W/2])
    pos_I = np.array([0, W/2])
    new_pos_I_aux = np.array([vel_tan[1] * deltaT, W/2])
    if theta != 0:
        d = new_pos_D_aux - new_pos_I_aux
        # Intercección con eje de las ruedas inicial
        n = -d[1]/d[0] * new_pos_D_aux[0] + new_pos_D_aux[1]
        centro_giro = np.array([0, n])
        new_pos_D = R(theta).dot(pos_D - centro_giro) + centro_giro
        new_pos_I = R(theta).dot(pos_I - centro_giro) + centro_giro
    else:
        # En este caso particular, no hay rotación
        new_pos_D = new_pos_D_aux
        new_pos_I = new_pos_I_aux
    new_pos = (new_pos_D + new_pos_I)/2
    return np.array([new_pos[0], new_pos[1], theta])

def start(vel_ang, t_final):
    # Con respecto al eje de coordenadas local, el eje de ruedas corresponde a la recta X = 0
    t = 0
    pos = x_0[:2]
    theta = x_0[2]
    print(np.array([pos[0], pos[1], theta]))
    vel_ang1 = vel_ang
    while t < t_final:
        next_pos_X, next_pos_y, dtheta = avanzar(vel_ang1, deltaT)
        next_pos = np.array([next_pos_X, next_pos_y])
        # El nuevo vector pos hay que rotarlo según cuánto rotamos el auto antes
        pos = pos + R(theta).dot(next_pos)
        theta += dtheta
        print(np.array([pos[0], pos[1], theta]))
        t += deltaT
# ------------------------------

# ---------- 2.b ----------
def v_fun(v, t):
    dvdt = 1/m * (tau_R/r + tau_L/r - c*v)
    return dvdt

def w_fun(w, t):
    dwdt = 1/J * (L/2 * tau_R/r - L/2 * tau_L/r - b*w)
    return dwdt

def next_state(x_prev, deltaT):
    x0, y0, theta0, v0, w0 = x_prev
    t = np.linspace(0, deltaT, 2)
    v = odeint(v_fun, v0, t)
    w = odeint(w_fun, w0, t)
    
    def theta_fun(theta, t):
        dthetadt = w[-1][0]
        return dthetadt
    theta = odeint(theta_fun, theta0, t)
    
    def x_fun(x, t):
        dxdt = v[-1][0]*np.cos(theta[-1][0])
        return dxdt
    x = odeint(x_fun, x0, t)

    def y_fun(x, t):
        dydt = v[-1][0]*np.sin(theta[-1][0])
        return dydt
    y = odeint(y_fun, y0, t)

    return np.array([x[-1][0], y[-1][0], theta[-1][0], v[-1][0], w[-1][0]])
# ------------------------------

# ----- Manejo de inputs -----
def pedir_input(op):
    # op = der: Lado derecho
    if op == "der":
        try:
            phi = float(input(">>> Velocidad angular de la rueda \033[1mderecha\033[0m [rad/s] > "))
        except ValueError:
            print("Asegúrate de ingresar un valor nuérico en las unidades señaladas")
            phi = pedir_input(op)
        return phi
    # op = izq: Lado izquierdo
    elif op == "izq":
        try:
            phi = float(input(">>> Velocidad angular de la rueda \033[1mizquierda\033[0m [rad/s] > "))
        except ValueError:
            print("Asegúrate de ingresar un valor nuérico en las unidades señaladas")
            phi = pedir_input(op)
        return phi
    elif op == "time":
        try:
            t = float(input(">>> Tiempo que durará la simulación [s] > "))
        except ValueError:
            print("Asegúrate de ingresar un valor nuérico en las unidades señaladas")
            t = pedir_input(op)
        return t


def parte_a():
    # ----- Recibir inputs -----
    print("Inserte las velocidades de las ruedas del robot:")
    phi1_dot = pedir_input(op= "der")
    phi2_dot = pedir_input(op= "izq")
    t_final = pedir_input(op= "time")
    # La función avanzar devuelve la posición y orientación del auto después de un tiempo
    # Dadas las velocidades angulares de las ruedas, devuelve la posición del auto en un tiempo futuro
    # El estado final es con respecto al sistema de coordenadas local del auto inicialmente.
    x_final = avanzar((phi1_dot, phi2_dot), t_final)
    print(f"\nx(t= 0.0) = {x_0} || x(t= {t_final}) = {x_final}\n")
    # La función start avanza en pequeños intervalos deltaT
    start((phi1_dot, phi2_dot), t_final)

def parte_b():
    global tau_R
    global tau_L
    # Incluye roce, devuelve los estado del auto
    t_final = pedir_input(op= "time")
    tau_R = 100
    tau_L = 10
    print(state_0)
    state = state_0
    t = 0
    while t < t_final:
        state = next_state(state, deltaT)
        print(state)
        t += deltaT

if __name__ == "__main__":
    # ----- Constantes -----
    deltaT = 0.01

    # ----- Parámetros del robot -----
    L = 0.2   # Largo de la base [m]
    W = 3 # 0.1   # Ancho de la base [m]
    H = 0.15  # Alto de la base [m]
    r = 1 # 0.04  # radio de las ruedas [m]
    m = 2     # masa del cuerpo de la base [kg]
    J = m/12 * (L**2 + W**2)  # Momento de inercia de la base sobre el eje normal al plano [kg*m^2]
    c = 30    # roce aerodinámico y viscoso en sentido longitudinal [N/(m/s)]
    b = 40    # roce aerodinámico y viscoso en torno al eje de giro [Nm/(rad/s)]

    # ---- Parámetros iniciales -----
    # x = (x, y, theta)
    x_0 = np.array([0, 0, 0]) # Estado inicial del robot
    # state = (x, y, theta, v, w)
    state_0 = np.array([0, 0, 0, 0, 0])

    # ----- Iniciar a -----
    # parte_a()

    # ----- Iniciar b -----
    parte_b()