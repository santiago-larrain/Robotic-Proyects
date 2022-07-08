from matplotlib import matplotlib_fname
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint


# Parámetros del sistema
I = 10**-3    # [kg*m^2]
b = 2*10**-3  # [Nm/rad/s]
m = 0.1       # [kg]
l = 0.1       # [m]
g = 9.81      # [m/s^2]
tau_0 = 0.01  # [Nm]

# Parámetros de la EDO
Wn = np.sqrt(m*g*l/I)
Z = b/(2*Wn*I)

def u(t):
    if t < 0:
        return 0
    else:
        return 1

def theta_fun(theta_vector, t):
    # La varible auxiliar rho es la primera derivada del ángulo con respecto al tiempo (theta')
    rho = theta_vector[0]
    theta = theta_vector[1]
    # La edo de segundo orden se puede dividir en dos edos de primer orden:
    # theta'' + 2*Z*Wn*theta' + Wn^2*sin(theta) = Tau   // t >= 0
    # theta'' = rho'
    # theta' = rho
    dtheta_dt = rho
    # rho' = Tau - 2*Z*Wn*rho - Wn^2*theta
    drho_dt = Tau*u(t)/I - Wn**2 * np.sin(theta) - 2*Z*Wn * rho
    return [drho_dt, dtheta_dt]

def modelar():
    theta_0 = [0.0, 0.0]   # theta'(t = 0), theta(t = 0)
    t = np.linspace(-1, 5, 1000)
    # Pénduolo
    sol = odeint(theta_fun, theta_0, t)
    th = sol[:, 1]
    plt.plot(t, th)
    plt.title(f"Posición angular ante un torque externo Tau = {Tau}Nm")
    plt.xlabel("tiempo [s]")
    plt.ylabel("theta [rad]")

    ## Preguntas:
    # Tiempo de subida (10% -> 90%) (theta_f = Tau/(I*Wn^2))
    k = 0
    while th[k] < 0.10*Tau/(I*Wn**2):
        k += 1
    tr_inicial = t[k]
    k = 0
    while th[k] < 0.90*Tau/(I*Wn**2):
        k += 1
    tr_final = t[k]
    print(f"> tr = {round(tr_final - tr_inicial, 5)} s")

    # Porcentaje de sobreoscilación (Mp_inicial = objetivo)
    Mp_inicial = Tau/(I*Wn**2)
    k = 0
    while sol[k][0] >= 0:
        k += 1
    Mp_final = th[k]
    print(f"> Mp = {round((Mp_final - Mp_inicial)/Mp_inicial*100, 5)} %")

    # Tiempo de establecimiento
    dtheta_dt_prev = sol[0][0]
    for time, dtheta_dt, theta in zip(t, sol[:, 0], sol[:, 1]):
        # En un cerro (cambio de signo de la derivada), que la diferencia sea menor o igual al 1%
        if np.sign(dtheta_dt) != np.sign(dtheta_dt_prev) and abs((theta - Mp_inicial)/Mp_inicial) <= 0.01:
            print(f"> ts = {round(time, 5)} s")
            break
        dtheta_dt_prev = dtheta_dt

    # Valor en régime permanente
    t_f = np.linspace(0, 1000, 1001)
    theta_final = odeint(theta_fun, theta_0, t_f)[-1][1]
    print(f"> Theta_f = {round(theta_final, 5)} rad")

if __name__ == "__main__":
    # Se pueden modelar múltiples torques aplicados para observar los movimientos del péndulo
    TAU = [tau_0]
    for Tau in TAU:
        print(f"\nTau = {Tau}Nm")
        modelar()
    print("")
    
    plt.show()