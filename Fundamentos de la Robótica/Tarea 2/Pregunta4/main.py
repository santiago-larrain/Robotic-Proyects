from math import asin
from time import sleep
import numpy as np
from scipy.integrate import odeint
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)

# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
scale = 300

pygame.init()   # Start pygame
# pygame.display.set_mode()
screen = pygame.display.set_mode((XMAX,YMAX))   # Display the window.
                                                # This creates a so-called
                                                # 'drawing surface' or simply
                                                # 'Surface'.
pygame.display.set_caption('Robotic Arm')   # Set the window's title
pygame.key.set_repeat(1,50)  # Works with essentially no delay, i.e.
                            # keeping a key pressed generates a continuous
                            # sequence of inputs and does not require the
                            # the user to release the keyboard to input
                            # characters as a repetition of key strokes.
#pygame.key.set_repeat(0,50) # Doesn't work because when the delay is set to
                            # zero, key.set_repeat is returned to the default,
                            # disabled state

def initialize_screen():
        # Fill the screen with a dark blue color to use it as background color.
        screen.fill((0,0,63))
        ## Dibujar plano cartesiano:
        pygame.draw.line(screen, (200,200,200), np.array([XMAX/2, 10]), np.array([XMAX/2, YMAX - 10]), 1)
        pygame.draw.line(screen, (200,200,200), np.array([10, YMAX/2]), np.array([XMAX - 10, YMAX/2]), 1)
        # Malla que marca la unidad:
        for i in range(21):
            if i == 10:
                continue
            pygame.draw.line(screen, (100,100,100), np.array([10, YMAX/2 + 30*(i-10)]), np.array([XMAX - 10, YMAX/2 + 30*(i-10)]), 1)
            pygame.draw.line(screen, (100,100,100), np.array([XMAX/2 + 30*(i-10), 10]), np.array([XMAX/2 + 30*(i-10), YMAX - 10]), 1)

def mostrar_estado(tau):
    font = pygame.font.SysFont('Arial', 20)
    text_str = f"Torque rueda Derecha: {round(tau[0]*10**5)/10**5} [Nm]"
    screen.blit(font.render(text_str, True, (200,200,200)), (5, 5))
    text_str = f"Torque rueda Izquierda: {round(tau[1]*10**5)/10**5} [Nm]"
    screen.blit(font.render(text_str, True, (200,200,200)), (5, 28))
    text_str = f"Velocidad: {round(robot_movil.state[3]*10**5)/10**5} [m/s]"
    screen.blit(font.render(text_str, True, (200,200,200)), (5, 50))

# Clase de cada punto por el que se moverá el brazo
class Robot():

    def __init__(self, estado):
        self.state = estado
        self.pos = np.array([estado[0], estado[1]])
        self.orientacion = estado[2]
        self.origen = np.array([XMAX/2, YMAX/2])
        # Las siguientes coordenadas con con respecto al origen del plano(0,0)
        self.esquinas = np.array([ np.array([-L/2, W/2]),
                                    np.array([-L/2, -W/2]),
                                    np.array([L/2, -W/2]),
                                    np.array([L/2, W/2]) ])
        self.esquinas_rueda_L = np.array([ np.array([-1/6*L, 2/3*W]),
                                            np.array([-1/6*L, W/2]),
                                            np.array([1/6*L, W/2]),
                                            np.array([1/6*L, 2/3*W]) ])
        self.esquinas_rueda_R = np.array([ np.array([-1/6*L, -2/3*W]),
                                            np.array([-1/6*L, -W/2]),
                                            np.array([1/6*L, -W/2]),
                                            np.array([1/6*L, -2/3*W]) ])
        self.esquinas_parachoque = np.array([ np.array([9/20*L, W/2]),
                                                np.array([9/20*L, -W/2]),
                                                np.array([L/2, -W/2]),
                                                np.array([L/2, W/2]) ])
        self.color = (200, 100, 100)
        self.color_rueda = (100, 200, 100)
        self.color_parachoque = (100, 100, 200)
        self.lunched_disc = False
        self.disc = Disco()

    def dibujar(self):
        pygame.draw.polygon(screen, self.color, self.ajustar(self.esquinas), 0)
        pygame.draw.polygon(screen, self.color_rueda, self.ajustar(self.esquinas_rueda_L), 0)
        pygame.draw.polygon(screen, self.color_rueda, self.ajustar(self.esquinas_rueda_R), 0)
        pygame.draw.polygon(screen, self.color_parachoque, self.ajustar(self.esquinas_parachoque), 0)
    
    def ajustar(self, matrix):
        # Toma un set de puntos para dibujar y los rota según la orientación del auto, luego los desplaza según la posición del auto
        # y finalmente lo desplaza en la pantalla. OJO con invertir la posición del auto en el eje Y y escalar los puntos
        new_matrix = []
        for point in matrix:
            new_point = R(self.orientacion).dot(point) + self.pos
            new_point = np.array([new_point[0], -new_point[1]])
            new_point = new_point*scale + self.origen
            new_matrix.append(new_point)
        return np.array(new_matrix)
    
    def actualizar(self, dt, tau):
        # Se trabaja en coordenadas cartesianas, pero al dibujar hay que escalar y trasladar los vectores
        # Actualiza el estado del auto robótico con el modelo dinámico
        # Por maña de python, si el auto no tiene velocidad y no hay torque, no se buscará otro estado
        if abs(self.state[3]) >= 1e-4 or tau.any():
            self.state = next_state(self.state, dt, tau[0], tau[1])
        self.pos = np.array([self.state[0], self.state[1]])
        self.orientacion = self.state[2]
        if not self.lunched_disc:
            self.disc.pos = self.pos
    
    def lunch_disc(self):
        if self.lunched_disc:
            print("I'm out of ammo!")
        else:
            print("Blam!")
            self.disc.direction = R(self.orientacion).dot(np.array([1,0]))
            self.disc.velocidad_auto = self.state[3]
            self.lunched_disc = True
        
    def reset_disc(self):
        print("Reloading!")
        self.disc = Disco()
        self.disc.pos = self.pos
        self.lunched_disc = False
    
    def reiniciar(self):
        self.state = initial_state
        self.reset_disc()
    
class Disco():

    def __init__(self):
        self.origen = np.array([XMAX/2, YMAX/2])
        self.pos = ()
        self.direction = ()   # Siempre unitario
        self.velocidad_auto = 0
        self.color = (150, 200, 200)
        self.color2 = (0, 0, 150)
        self.visibile = True
    
    def avanzar(self):
        # Dinámica básica, el disco también tiene la velocidad del auto
        self.pos = self.pos + self.direction*(velocidad_disco + self.velocidad_auto)*deltaT
        if (self.ajustar() < 0).any() or (self.ajustar() > np.array([XMAX, YMAX])).any():  
            self.visibile = False

    def dibujar(self):
        pygame.draw.circle(screen, self.color, self.ajustar(), 10, 10)
        pygame.draw.circle(screen, self.color2, self.ajustar(), 7, 2)
    
    def ajustar(self):
        # Se trabaja en coordenadas cartesianas, pero al dibujar hay que escalar y trasladar los vectores
        # Devuelve su posición en la pantalla
        new_point = np.array([self.pos[0], -self.pos[1]])
        new_point = new_point*scale + self.origen
        return new_point

def revisar_eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                    #  http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            return "reset" # reset the program by execute the program again
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            return np.array([-dTau, 0])
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            return np.array([dTau, 0])

        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            return np.array([0, -dTau])

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            return np.array([0, dTau])

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            return ("stop")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return ("lunch")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            return ("automatic")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            return ("help")

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            return ("point", (screen, (150, 50, 255), mouse_pos, 7, 7))
    
    return False

def R(t):
    # Matriz de rotación para un ángulo t en radianes.
    return np.array([[np.cos(t), -np.sin(t)], 
                     [np.sin(t), np.cos(t)]])

def buscar_tau(r, dphi):
    tau_aux = 0
    tau_L = 0
    error_w = dphi
    ponderador = 10**3
    
    # Primero determinamos el error en el ángulo, pues con este determinamos la rotación y con ello, la relación entre los torques que debe haber
    while abs(error_w) >= 1e-5:
        state = next_state(robot_movil.state, deltaT, tau_aux, tau_L)
        w = state[4]
        error_w = dphi - w*deltaT
        tau_aux += error_w*ponderador
    
    # Nos interesa movernos hacia adelante (v >= 0)
    error_v = abs(r*dphi)
    # Ahora que encontramos el delta(Tau) que debe haber, comenzemos en v = 0 y umentemos los torques hasta que v = r*phi
    # Comienzo en v = 0 (tau_R = -Tau_L, tau_R - tau_L = tau_aux)
    tau_R = tau_aux/2
    tau_L = -tau_aux/2
    ponderador = 10**2
    while abs(error_v) >= 1e-5:
        state = next_state(robot_movil.state, deltaT, tau_R, tau_L)
        v = state[3]
        error_v = abs(r*dphi) - v*deltaT
        tau_R += error_v*ponderador
        tau_L += error_v*ponderador
    # Exagero la diferencia para girar más rápido, pero mantengo la velocidad
    return tau_R, tau_L
    dif = tau_R - tau_L
    if dif > 0:
        tau_R += dif
    else:
        tau_L += -dif
    return tau_R, tau_L

def circunferencia(theta, A, P):
    # theta = orientación del auto
    # A = Posición del auto
    # P = Punto objetivo
    ax, ay = A
    px, py = P
    # Ver archivo Wolfram para comprender de dónde vienen estas ecuaciones
    cx = (px**2 + py**2 - ax**2 - ay**2) / (2*(ax - px + (py - ay)/np.tan(theta)))
    cy = -(px**2 + py**2 - ax**2 - ay**2)/(2*(ay - py)) - ((ax - px)*(px**2 + py**2 - ax**2 - ay**2))/(2*(ay - py)*(ax - px + (py - ay)/np.tan(theta)))
    r = np.sqrt((ax - cx)**2 + (ay - cy)**2)
    # Se entregan las coordenadas de la circunferencia en coordenadas polares
    return r

def automatic(P):
    # --- Disclaimer ---
    # Este código automático fue escrito en 1:37 hrs a las 00:00, incluyendo todo el pensamiento lógico que hay detrás,
    # por lo que es probable haber pasado algunas condiciones.
    # Para futura mejora, lo que hace es buscar un círculo talque su centro equidista al punto y al auto y además, es tangente a la orientación del auto.
    # De este modo, encuentra un camino óptimo curvo cuya curvatura mejora a medida que avanza. Sin embargo, tiene fallas por mejorar.
    theta = robot_movil.orientacion
    A = robot_movil.pos
    r = circunferencia(theta, A, P)
    dphi_dt = 10  # velocidad en [rad/s]
    # Si el giro debe ser positivo, se utilizará un dphi negativo. El signo de giro se puede determinar con el producto A x B, el cual solo 
    # tendrá componente Z y si es positivo, entonces hay que girar hacia la izquierda (positivo) y, en caso contrario, a la derecha (negativo)
    A2D = R(theta).dot(np.array([1, 0]))
    A = np.array([A2D[0], A2D[1], 0])
    B2D = P - robot_movil.pos
    B = np.array([B2D[0], B2D[1], 0])
    Area = np.cross(A, B)[2]
    desfase = np.arcsin(Area/(np.linalg.norm(A)*np.linalg.norm(B)))
    P_norm = np.linalg.norm(B)
    '''
    tau_R, tau_L = buscar_tau(r*min(1, P_norm), np.sign(Area)*min(5, max(abs(Area)*(1+P_norm)**2,0.1))*dphi_dt*deltaT, 0)
    # Evitar aceleración excesiva
    if tau_R >= 50 or tau_L >= 50:
        tau_R = tau_R/10**(len(str(round(tau_R))) - 1)
        tau_L = tau_L/10**(len(str(round(tau_L))) - 1)
    '''
    tau_R, tau_L = buscar_tau(r*np.expm1(P_norm), dphi_dt*deltaT*desfase)
    return np.array([tau_R, tau_L])

def next_state(x_prev, deltaT, tau_R, tau_L):
    # Función de dinámica de auto con tracción diferencial
    x0, y0, theta0, v0, w0 = x_prev
    t = np.linspace(0, deltaT, 2)
    
    def v_fun(v, t):
        dvdt = 1/m * (tau_R/r + tau_L/r - c*v)
        return dvdt
    v = odeint(v_fun, v0, t)

    def w_fun(w, t):
        dwdt = 1/J * (L/2 * tau_R/r - L/2 * tau_L/r - b*w)
        return dwdt
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

def main(dt, tau, point):
    # Pantalla y plano cartesiano
    initialize_screen()
    
    robot_movil.actualizar(dt, tau)
    # El disco se mueve por su cuenta si es lanzado
    if robot_movil.lunched_disc:
        robot_movil.disc.avanzar()
        # Al salirse de la pantalla, se recarga el disco en el auto
        if not robot_movil.disc.visibile:
            robot_movil.reset_disc()
    
    # Dibujar auto y disco
    robot_movil.dibujar()
    robot_movil.disc.dibujar()
    # Dibujar punto si este existe
    if point:
        if point[0] != "Ka-Boom":
            pygame.draw.circle(*point)
            # Revisar si el disco alcanzó al punto
            point_pos = np.array([point[2][0], point[2][1]])
            if robot_movil.lunched_disc:
                if np.linalg.norm(robot_movil.disc.ajustar() - point_pos) <= 15:
                    robot_movil.reset_disc()
                    # Efectos especiales, por un breve tiempo se sibujará una explosión
                    poligono1 = []
                    poligono2 = []
                    t = np.pi/2
                    for i in range(5):
                        corner = R(t).dot(np.array([0, 25]))
                        corner = corner + point_pos
                        poligono1.append(corner)
                        t += 4/5*np.pi
                    for i in range(5):
                        corner = R(t).dot(np.array([0, 15]))
                        corner = corner + point_pos
                        poligono2.append(corner)
                        t += 4/5*np.pi
                    print("POW!!!")
                    return ("POW", (screen, (255, 0, 0), poligono1, 15), (screen, (255, 174, 66), poligono2, 10))
        else:
            # Dibujar explosión
            pygame.draw.polygon(*point[1])
            pygame.draw.polygon(*point[2])
    mostrar_estado(tau)
    
    pygame.display.flip()
    
    return point

def start():
    print(">>> Para salir del juego presiona \033[1mEsc\033[0m")
    print(">>> Para pedir ayuda presiona \033[1mH\033[0m")
    tau = np.array([0, 0])
    stop = False
    auto = False
    point = None
    stop_timer = 0
    pow_timer = 0
    auto_timer = 0
    help_timer = 0
    deltaT = 0.01
    while True:
        # main es el código que implementa los cambios en cada iteración, actualizando también la pantalla
        point = main(deltaT, tau, point)

        # Caso de choque, explosión de 0.15s
        if point:
            if point[0] == "POW":
                pow_timer = 0
                point = ("Ka-Boom", point[1], point[2])
            if point[0] == "Ka-Boom" and pow_timer >= 0.15:
                point = None
        # Manejo de teclado (ver la función respectiva)
        op = revisar_eventos()
        if type(op) != bool:
            if type(op[0]) != str:
                tau = tau + op
            else:
                if op == "stop" and stop_timer >= 0.2:
                    stop = not stop
                    stop_timer = 0
                elif op == "reset":
                    stop = False
                    tau = np.array([0, 0])
                    robot_movil.reiniciar()
                    point = None
                    auto = False
                elif op == "lunch":
                    robot_movil.lunch_disc()
                elif op == "automatic":
                    if auto_timer >= 0.2:
                        auto = not auto
                        auto_timer = 0
                        if auto:
                            stop = False
                elif op[0] == "point":
                    point = op[1]
                elif op == "help" and help_timer >= 0.2:
                    help_timer = 0
                    print("-"*50)
                    print(">>> Para avanzar utiliza las flechas: \033[1mUp/Down\033[0m para manipular el torque de la rueda derecha" +\
                        "y \033[1mRight/Left\033[0m para manipular el torque de la rueda izquierda")
                    print(">>> Para \033[1mfrenar\033[0m presiona la tecla \033[1mS\033[0m")
                    print(">>> Para \033[1mactivar/desactivar\033[0m el modo automático presiona la tecla \033[1mA\033[0m")
                    print(">>> Para \033[1mmarcar un punto\033[0m oprime \033[1mclick izquierdo\033[0m en la pantalla")
                    print(">>> Para \033[1mdisparar el disco\033[0m presiona la \033[1mbarra espaciadora\033[0m")
                    print(">>> Para \033[1mreiniciar\033[0m el juego presiona la tecla \033[1mEnter\033[0m")
                    print(">>> Para \033[1msalir\033[0m del juego presiona la tecla \033[1mEsc\033[0m")
                    print("-"*50)
        
        # Si se tiene el freno de mano puesto, no hay torque
        if stop:
            tau = np.array([0, 0])
        else:
            if auto and point:
                if type(point[0]) != str:
                    Px, Py = point[2]
                    Px = (Px - XMAX/2)/scale
                    Py = (YMAX/2 - Py)/scale
                    P = np.array([Px, Py])
                    if np.linalg.norm(robot_movil.pos - P) <= 0.02:
                        tau = np.array([0, 0])
                        point = None
                    else:
                        tau = automatic(P)
        
        stop_timer += deltaT
        pow_timer += deltaT
        auto_timer += deltaT
        help_timer += deltaT
        sleep(deltaT)


if __name__ == '__main__':
    # ----- Constantes -----
    deltaT = 0.01
    velocidad_disco = 1.5  # [m/s]
    dTau = 0.2           # Cambio en torques al aplicar flechas

    # ----- Parámetros del robot -----
    L = 0.2   # Largo de la base [m]
    W = 0.1   # Ancho de la base [m]
    H = 0.15  # Alto de la base [m]
    r = 0.04  # radio de las ruedas [m]
    m = 2     # masa del cuerpo de la base [kg]
    J = m/12 * (L**2 + W**2)  # Momento de inercia de la base sobre el eje normal al plano [kg*m**2]
    c = 30    # roce aerodinámico y viscoso en sentido longitudinal [N/(m/s)]
    b = 40    # roce aerodinámico y viscoso en torno al eje de giro [Nm/(rad/s)]

    # ------------------------------
    # La grilla tiene unidades marcadas cada 0.1 m, teniéndose una pantalla total de 2x1.5 m
    # El tamaño del mapa y la escala se puede modificar en el inicio del código
    initial_state = np.array([0, 0, 0, 0, 0])
    robot_movil = Robot(initial_state)
    start()