import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

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

def control_PID(Tau_prev, k, errores):
    err_actual, err_prev, err_pprev = errores
    kp, ki, kd = k
    k0 = kp*(1 + Ts*ki + kd/Ts)
    k1 = -kp*(1 + 2*kd/Ts)
    k2 = kp*kd/Ts
    return Tau_prev + k0*err_actual + k1*err_prev + k2*err_pprev

def control_bang_bang(actual_value, valor, rango):
    if valor < ref(0) - rango:
        return Tau_On
    elif valor > ref(0) + rango:
        return 0
    return actual_value

def u(t):
    if t >= 0:
        return 1
    else:
        return 0

def ref(t):
    if t >= 0:
        return np.pi/18
    else:
        return 0

def print_valores(time, th, dth_dt):

    # Tiempo de subida (10% -> 90%) (theta_f = promedio de valores)
    try:
        k = 0
        while th[k] < 0.10*ref(0):
            k += 1
        tr_inicial = time[k]
        while th[k] < 0.90*ref(0):
            k += 1
        tr_final = time[k]
    except IndexError:
        pass
    else:
        print(f"> tr = {round(tr_final - tr_inicial, 5)} s")

    # Porcentaje de sobreoscilación
    k = 0
    while dth_dt[k] >= 0:
        k += 1
    Mp_final = th[k]
    if Mp_final > ref(0):
        print(f"> Mp = {round((Mp_final - ref(0))/ref(0)*100, 5)} %")

    # Tiempo de establecimiento
    dtheta_dt_prev = dth_dt[0]
    for ti, dtheta_dt, theta in zip(time, dth_dt, th):
        # En un cerro (cambio de signo de la derivada), que la diferencia sea menor o igual al 1%
        if (np.sign(dtheta_dt) != np.sign(dtheta_dt_prev) or abs(dtheta_dt) <= 1e-6) and abs((theta - np.mean(th[int(t_final*frecuency*importante):]))/np.mean(th[int(t_final*frecuency*importante):])) <= 0.01:
            print(f"> ts = {round(ti, 5)} s")
            break
        dtheta_dt_prev = dtheta_dt
    # Valor en régimen permanente y su error (la mejor estimación es el promedio de los datos después de un rato)
    print(f">> theta final = {np.mean(th[int(t_final*frecuency*importante):])}")
    print(f">> error permanente = {round(abs(ref(0) - np.mean(th[int(t_final*frecuency*importante):]))/ref(0)*100, 5)}%\n")

if __name__ == "__main__":
    # --- Parámetros iniciales ---
    frecuency = 10000      # 10000 Hz | presición de 4 decimales en tiempo
    Ts = 1/frecuency       # 0.1 ms
    importante = 2/3       # Solo importa, para el valor estable, el último tercio de la simulación

    # --- Parámetros del sistema ---
    I = 10**-3    # [kg*m^2]
    b = 2*10**-3  # [Nm/rad/s]
    m = 0.1       # [kg]
    l = 0.1       # [m]
    g = 9.81      # [m/s^2]

    # --- Parámetros de la EDO ---
    Wn = np.sqrt(m*g*l/I)
    Z = b/(2*Wn*I)

    # --- Inicilaizador ---
    Tau = 0
    theta = [0.0, 0.0]       # dTheta/dt, Theta
    error = (0, 0, 0)    # error_actual, error_previo, error_previo_previo

    tipo = int(input("Contorlador Proporcional (1), Proporcional-Derivativo (2) o Bang-Bang (3): "))
    if tipo == 1:
        name = "Proporcional"
        t_final = 10
        # --- Parámetros del controlador PID ---
        K_pid = (0.1344, 0, 0)    # Mp < 5% | Error permanente = 42% | ts = 9,5s
        # NUNCA: ts < 500 ms | Error Permanente < 1% --> Siempre habrá error permanente
    elif tipo == 2:
        name = "Proporcional-Derivativo"
        t_final = 0.5
        # --- Parámetros del controlador PID ---
        K_pid = (40, 0, 0.038)     # Mp < 5% | Error Permanente < 1% | ts < 500 ms
    elif tipo == 3:
        name = "Bang-Bang"
        t_final = 10
        on = False
        # Error Permanente < 1% | ts = 7.7s | Mp = 38%
        Tau_On = 0.02
        precision = np.pi/180*0.001    # [rad] --> 0.001°


    # --- Loop de 500 ms ---
    time = []
    pos = []
    dpos_dt = []
    t = 0
    while t <= t_final:
        if tipo != 3:
            Tau = control_PID(Tau, K_pid, error)
        else:
            Tau = control_bang_bang(Tau, theta[1], precision)
        theta = odeint(theta_fun, theta, np.linspace(t, t+Ts, 3))[1]
        
        time.append(t)
        pos.append(theta[1])
        dpos_dt.append(theta[0])

        # --- Actualizar ---
        # error[0] = error_actual (previo) = error_previo
        # error[1] = error_previo (previo) = error_previo_previo
        error = (ref(t) - theta[1], error[0], error[1])
        t += Ts
        
    # Porcentaje de sobre-oscilación
    # El centro de oscilación se puede estimar como el promedio de las sobre-oscilaciones
    print_valores(time, pos, dpos_dt)
    plt.plot(time, pos)
    plt.title(f"Control {name} | Ref = {round(ref(0), 3)} rad")
    plt.xlabel("tiempo [s]")
    plt.ylabel("theta [rad]")
    plt.show()