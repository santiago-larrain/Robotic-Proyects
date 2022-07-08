from plot_data_P1 import graficar_datos
import numpy as np
from time import sleep
import csv
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)

# --- Archivo exportado ---
## OJO: El archivo main.py debe correrse de tal forma que el archivo "Resultados_brazo.csv" se cree en el mismo directorio que este archivo.
##      De este modo, el archivo plot_data_P1.py podrá encontrarlo y leer sus datos.
field_names = ["t [s]", "Q [rad]", "W [rad/s]", "A [rad/s^2]", "P_dot [m/s]", "P_ddot [m/s^2]"]
def exportar(estados):
    # estados es una lista con diccionarios de cada fila (estado) para cada tiempo
    # Esta función solo se llama una vez y es al llegar al segundo punto marccado
    nombre_archivo = "Resultados_brazo.csv"
    file = open(nombre_archivo, "w", encoding= "utf-8")
    writer = csv.DictWriter(file, fieldnames= field_names)
    writer.writeheader()
    writer.writerows(estados)
    file.close()
    # Pedirle al archivo plot_data.py que grafique los datos recolectados
    graficar_datos(nombre_archivo, field_names)

def agregar_estado(data, t, Q, W, A, P_dot, P_ddot):
    # Recibe un estado y lo añade a la lista que más tarde pasará a el archivo csv
    fn = field_names
    data.append({fn[0]: t, fn[1]: f"{Q[0]},{Q[1]}", fn[2]: f"{W[0]},{W[1]}", fn[3]: f"{A[0]},{A[1]}", 
                 fn[4]: f"{P_dot[0]},{P_dot[1]}", fn[5]: f"{P_ddot[0]},{P_ddot[1]}"})
    return data


# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
scale_line = 200
ponderador = 1  # Ponderador de velocidad del brazo al recorrer la trayectoria entre puntos

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
        ## Dibujar límites del robót:
        pygame.draw.circle(screen, (100, 100, 150), np.array([XMAX/2, YMAX/2]), (l1 + l2)*scale_line, 1)
        pygame.draw.circle(screen, (100, 100, 150), np.array([XMAX/2, YMAX/2]), (l1 - l2)*scale_line, 1)
        ## Dibujar plano cartesiano:
        pygame.draw.line(screen, (200,200,200), np.array([XMAX/2, 10]), np.array([XMAX/2, YMAX - 10]), 1)
        pygame.draw.line(screen, (200,200,200), np.array([10, YMAX/2]), np.array([XMAX - 10, YMAX/2]), 1)
        # Malla que marca la unidad:
        for i in range(21):
            if i == 10:
                continue
            pygame.draw.line(screen, (100,100,100), np.array([10, YMAX/2 + 30*(i-10)]), np.array([XMAX - 10, YMAX/2 + 30*(i-10)]), 1)
            pygame.draw.line(screen, (100,100,100), np.array([XMAX/2 + 30*(i-10), 10]), np.array([XMAX/2 + 30*(i-10), YMAX - 10]), 1)

# Clase de cada punto por el que se moverá el brazo
class Punto():

    def __init__(self, coordenadas) -> None:
        self.pos = np.array([coordenadas[0], coordenadas[1]])
        self.objective = None    # Si el brazo está en este objeto, se moverá hacia el objetivo respectivo
        self.objetivo_alcanzado = False   # bool que indica si se ha llegado al objetivo de este punto
        self.tiempo_mov = 0
    
    def dibujar(self):
        pygame.draw.circle(screen, (0, 150, 0), self.pos, 4, 3)  # Dibujar el punto
    
    def retornar_objetivo_ultimo(self):
        # Esta función devuelve el siguiente objetivo hasta el último para agregar un nuevo objetivo a la cadena
        if self.objective == None:
            return self
        else:
            return self.objective.retornar_objetivo_ultimo()
    
    def buscar_siguiente(self):
        if self.objetivo_alcanzado:
            return self.objective.buscar_siguiente()
        else:
            return self

    def calcular_dreccion(self):
        # Determina d: vector director entre el objeto y su objetivo
        return (self.objective.vector() - self.vector()) / np.linalg.norm(self.objective.vector() - self.vector())

    def tiempo_por_salto(self):
        # Permite determinar el tamaño de salto para moverse idealmente en 1 segundo de principio a fin
        # Cada vez que se llame, el t aumenta. t se mueve entre 0 y ||P*-P0||
        # Desacelerar al llegar y acelerar al partir
        self.tiempo_mov += deltaT

        # Una vez se llega a la última iteración, se llega al objetivo.
        if np.linalg.norm(self.objective.vector() - self.vector()) - self.tiempo_mov < deltaT:
            # El siguiente punto será el objetivo, hasta que se llegue a él
            self.tiempo_mov = np.linalg.norm(self.objective.vector() - self.vector())
        return self.tiempo_mov

    def vector(self):
        # Devuelve el punto como un vector centrado en el origen y escalonado a los otros vectores
        return (np.array([self.pos[0], -self.pos[1]]) + np.array([-XMAX/2, YMAX/2])) / scale_line
    
    def next_mov(self):
        siguiente_punto = self.calcular_dreccion() * self.tiempo_por_salto() + self.vector()
        ###################### EN MANTENCIÓN ######################
        # Revisar si el brazo pasa por el círculo interno (No puede alcanzarlo por limitaciones físicas)
        # if np.linalg.norm(siguiente_punto) <= l1-l2 + 0.001:
        #     # Entrego el siguiente punto y su dirección; me devuelve un punto ortogonal a la dirección 
        #     # que está en la zona factible, solo alejada un deltaT * ponderador de los límites físicos 
        #     # para que el brazo llegue a él
        #     self.divisor = (deltaT * ponderador)**2  # Para el próximo salto
        #     siguiente_punto = rodear_circulo(siguiente_punto, siguiente_punto - self.vector())
        # self.divisor = deltaT * ponderador
        ###########################################################
        return siguiente_punto

    def reiniciar(self):
        self.objective = None
        self.objetivo_alcanzado = False
        self.tiempo_mov = 0
    
def revisar_eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                    #  http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            start() # reset the program by execute the program again
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Revisar que el punto sea factible (El brazo robótico lo pueda alcanzar)
            if np.sqrt((mouse_pos[0] - XMAX/2)**2 + (mouse_pos[1] - YMAX/2)**2) <= (l1+l2)*scale_line and \
                np.sqrt((mouse_pos[0] - XMAX/2)**2 + (mouse_pos[1] - YMAX/2)**2) >= (l1-l2)*scale_line :
                # Esto le asigna a cada punto el que le sigue.
                last = brazo.retornar_objetivo_ultimo()
                last.objective = Punto(mouse_pos)
# ----- Prototipo. No implementado -----
# Las funciones intercepción y rodear_circulo permiten que el brazo rodee al círculo interno cuando se traza una linea que lo atraviese.
# La idea de estas funciones es que el brazo tome un camino factible óptimo (rodear este círculo) a fin de no volverse loco por no poder alcanzar el punto objetivo.
# Sin embargo, las funciones tienen fallas y no está listas aún. Para futuro, una opción sería esperar a que el brazo se envuelva (q2 = 180°) y luego
# solo variar q1 hasta que se haya dado la vuelta al círculo y continuar con el flujo del programa. No se implementa por temas de tiempo, pero la idea
# se ve prometedora.
def intercepcion(m, n, x_0):
    # Esta función busca la intercepción de una recta con el límite interno del brazo
    delta = 0.000001
    opciones = []
    if m != "Infinity":
        x = x_0
        y = m*x + n
        # Buscar hacia la derecha
        while (x**2 + y**2)**(1/2) <= l1-l2 + 0.001:
            x += delta
            y = m*x + n
        opciones.append(np.array([x, y]))
        # Buscar hacia la izquierda
        x = x_0
        while (x**2 + y**2)**(1/2) <= l1-l2 + 0.001:
            x -= delta
            y = m*x + n
        opciones.append(np.array([x, y]))
    # Caso de recta vertical
    else:
        y = x_0
        x = n  # x = constante
        # Buscar hacia arriba
        while (x**2 + y**2)**(1/2) <= l1-l2 + 0.001:
            y += delta
        opciones.append(np.array([x, y]))
        # Buscar hacia la izquierda
        y = x_0
        while (x**2 + y**2)**(1/2) <= l1-l2 + 0.001:
            y -= delta
        opciones.append(np.array([x, y]))
    
    return opciones

def rodear_circulo(punto, direccion):
    # Buscamos A = (ax, ay) talque D.A = 0 (D = direccion)
    # dx*ax + dy*ay = 0 || ay = -dx/dy * ax || pendiente m = -dx/dy
    dx, dy = direccion
    px, py = punto
    if dy != 0:
        # Mucha mátemática, pero en resumen, el desplazamiento de la recta se define del siguiente modo:
        # Corroborar que no haya división por cero; en esos caso la arctan puede ser -Pi/2 o Pi/2
        try:
            theta = np.arctan(py/px)
        except ZeroDivisionError:
            if py < 0:
                theta = -np.pi/2
            else:
                theta = np.pi/2
        try:
            psi = np.arctan(dy/dx)
        except ZeroDivisionError:
            if dy < 0:
                psi = -np.pi/2
            else:
                psi = np.pi/2
        ## Sí funciona...
        n = np.linalg.norm(punto) * np.sin((np.pi/2 + psi - theta)) / np.sin(np.pi - psi)
        # x_0 es el x del punto
        opciones = intercepcion(-dx/dy, n, x_0= px)
    else:
        # Caso particular de pendiente infinita
        # x es constante, y varía
        opciones = intercepcion("Infinity", px, x_0= py)
    
    # Devolver el punto más cercano para optimizar el movimiento
    print("P =", punto, "\nd =", direccion, "Movs =", opciones)
    print(">>", np.linalg.norm(opciones[0] - punto), np.linalg.norm(opciones[1] - punto))
    if np.linalg.norm(opciones[0] - punto) <= np.linalg.norm(opciones[1] - punto):
        print(">>>", 1)
        return opciones[0]
    else:
        print(">>>", 2)
        return opciones[1]
# --------------------------------------

def arreglo(l):
    # Esta funció arregla los vectores, pues hay que escalarlos para que sean visibles y 
    # además corregir el eje Y que está invertido
    lx, ly = l
    return np.array([lx, -ly])*scale_line + np.array([XMAX/2, YMAX/2])

def reducir(angulo):
    angulo_reducido = []
    for theta in angulo:
        while theta > 2*np.pi or theta < -2*np.pi:
            # Esta operación no cambia el ángulo, pues son vueltas completas.
            if theta >= 0:
                theta -= 2*np.pi
            else:
                theta += 2*np.pi
        # Esto permite minimizar la magnitud del ángulo haciendo que sea negativo si el positivo es mayor a 180 o viceversa
        if theta > np.pi:
            theta -= 2*np.pi
        elif theta < -np.pi:
            theta += 2*np.pi
        angulo_reducido.append(theta)
    return np.array(angulo_reducido)

def alcanzar_velocidad(w1, w2):
    # Haciendo que el cambio de velocidad dependa de cuánto le falta, servirá para optimizar el movimiento
    # Además, casos raros como cuando la velocidad se hace extremadamente grande, serán solucionados de forma rápida
    if w1 < w1_0:
        w1 += abs(w1 - w1_0)*deltaT
        ## Comprobar si nos pasamos
        if w1 > w1_0:
            w1 = w1_0
    elif w1 > w1_0:
        w1 -= abs(w1 - w1_0)*deltaT
        ## Comprobar si nos pasamos
        if w1 < w1_0:
            w1 = w1_0
    else:
        w1 += a1_0*deltaT

    if w2 < w2_0:
        w2 += abs(w2 - w2_0)*deltaT
        ## Comprobar si nos pasamos
        if w2 > w2_0:
            w2 = w2_0
    elif w2 > w2_0:
        w2 -= abs(w2 - w2_0)*deltaT
        ## Comprobar si nos pasamos
        if w2 < w2_0:
            w2 = w2_0
    else:
        w2 += a2_0*deltaT
    
    return w1, w2

def rad(theta):
    # La interfaz es en grados, pero el cálculo matemático debe ser en radianes; esta función hace el cambio
    return theta * np.pi / 180

def R(t):
    # Matriz de rotación para un ángulo t en grados.
    return np.array([[np.cos(rad(t)), -np.sin(rad(t))], 
                     [np.sin(rad(t)), np.cos(rad(t))]])

def angulos_optimos(p_optimo, q_inicial):
    ## p_optimo = [p*_x, p*_y]
    ## q_inicial = [q1, q2]

    def J_q(q_0):
        t_1 = rad(q_0[0])
        t_2 = rad(q_0[1])
        return np.array([[-l1*np.sin(t_1) - l2*np.sin(t_1 + t_2), -l2*np.sin(t_1 + t_2)],
                         [l1*np.cos(t_1) + l2*np.cos(t_1 + t_2), l2*np.cos(t_1 + t_2)]])

    epsilon = 1e-10
    q_viejo = q_inicial
    t1 = rad(q_viejo[0])
    t2 = rad(q_viejo[1])
    p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])

    q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)
    
    while (((p_optimo - p_actual) > epsilon).any() and \
            ((q_nuevo - q_viejo) > epsilon).any()):
        
        q_viejo = q_nuevo
        
        t1 = rad(q_viejo[0])
        t2 = rad(q_viejo[1])
        p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])
        
        q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)

    return q_nuevo

def seguir_linea(sig_posicion, Q_inicial):
    Q_final = angulos_optimos(sig_posicion, Q_inicial)
    P2_rotado = R(Q_final[0] + Q_final[1]).dot(np.array([l2, 0]))
    P1_rotado = R(Q_final[0]).dot(np.array([l1, 0]))
    P2_rot_tras = P1_rotado + P2_rotado
    
    return P1_rotado, P2_rot_tras, Q_final[0], Q_final[1]

def main(P, Q, W, W_dot, V, A):
    # Variables -------------
    p1_prev, p2_prev = P
    q1_prev, q2_prev = Q
    w1_prev, w2_prev = W
    w1_dot_prev, w2_dot_prev = W_dot
    v1_prev, v2_prev = V
    a1_prev, a2_prev = A
    # -----------------------

    ####################################################################################
    #### Funciones de dibujo, cada una está encargada de dibujar un tipo de vectores ###
    ####################################################################################
    
    def draw_arms(size_line):
        pygame.draw.line(screen, (200, 200, 200), arreglo((0,0)), arreglo(p1_prev), size_line)
        pygame.draw.line(screen, (150, 150, 150), arreglo(p1_prev), arreglo(p2_prev), size_line)
    
    # Vector velocidad P y sus componentes en base local y global:
    def velocidad_global(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1_prev + p1_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p1_prev), arreglo(np.array([v1_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v1_prev[0], 0]) + p1_prev), arreglo(v1_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2_prev + p2_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p2_prev), arreglo(np.array([v2_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v2_prev[0], 0]) + p2_prev), arreglo(v2_prev + p2_prev), size_line//2)

    def velocidad_local(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1_prev + p1_prev), size_line)
        v1b_proyectado = R(-q1_prev).dot(v1_prev)
        v1b_x = v1b_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (255, 150, 0), arreglo(p1_prev), arreglo(v1b_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (255, 150, 0), arreglo(v1b_x + p1_prev), arreglo(v1_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2_prev + p2_prev), size_line)
        v2b_proyectado = R(-(q1_prev + q2_prev)).dot(v2_prev)
        v2b_x = v2b_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (255, 150, 0), arreglo(p2_prev), arreglo(v2b_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (255, 150, 0), arreglo(v2b_x + p2_prev), arreglo(v2_prev + p2_prev), size_line//2)
        # -----------------------
    
    # Vector aceleración P y sus componentes en base global y local:
    def aceleracion_global(size_line):
        # P1
        pygame.draw.line(screen, (0, 0, 255), arreglo(p1_prev), arreglo(a1_prev + p1_prev), size_line)
        pygame.draw.line(screen, (0, 0, 150), arreglo(p1_prev), arreglo(np.array([a1_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 0, 150), arreglo(np.array([a1_prev[0], 0]) + p1_prev), arreglo(a1_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 0, 255), arreglo(p2_prev), arreglo(a2_prev + p2_prev), size_line)
        pygame.draw.line(screen, (0, 0, 150), arreglo(p2_prev), arreglo(np.array([a2_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 0, 150), arreglo(np.array([a2_prev[0], 0]) + p2_prev), arreglo(a2_prev + p2_prev), size_line//2)

    def aceleracion_local(size_line):
        # P1
        pygame.draw.line(screen, (0, 0, 255), arreglo(p1_prev), arreglo(a1_prev + p1_prev), size_line)
        a1b_proyectado = R(-q1_prev).dot(a1_prev)
        a1b_x = a1b_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (0, 150, 255), arreglo(p1_prev), arreglo(a1b_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 255), arreglo(a1b_x + p1_prev), arreglo(a1_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 0, 255), arreglo(p2_prev), arreglo(a2_prev + p2_prev), size_line)
        a2b_proyectado = R(-(q1_prev + q2_prev)).dot(a2_prev)
        a2b_x = a2b_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (0, 150, 255), arreglo(p2_prev), arreglo(a2b_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 255), arreglo(a2b_x + p2_prev), arreglo(a2_prev + p2_prev), size_line//2)
        # -----------------------

    ## Inicializar -----------------------------------------------------------------------------------------
    initialize_screen()
    draw_arms(10)
    # Velocidad -----------
    velocidad_global(4)
    #velocidad_local(4)
    # Aceleración ---------
    aceleracion_global(4)
    #aceleracion_local(4)
    ## -----------------------------------------------------------------------------------------------------
    
    revisar_eventos()
    # Mostrar los puntos seleccionados en la pantalla y 
    # luego las lineas entre ellos, las cuales serán seguidas por el brazo robótico
    point = brazo.objective
    while point != None:
        if not point.objetivo_alcanzado:    
            point.dibujar()
            if point.objective != None:
                pygame.draw.line(screen, (0, 150, 0), point.objective.pos, point.pos, 2)
        point = point.objective
    
    pygame.display.flip()
    
    ## Actualizar vectores posición --------------------------------------------------------------------------------
    # Si no hay puntos, seguir con el movimiento predefinido inicialmente
    actual = brazo.buscar_siguiente()
    if actual.objective != None:
        if actual == brazo and brazo.tiempo_mov == 0:
            brazo.pos = arreglo(p2_prev)
    
        p1, p2, q1, q2 = seguir_linea(actual.next_mov(), np.rad2deg(reducir(np.deg2rad(Q))))
        q1, q2 = np.rad2deg(reducir(np.deg2rad((q1, q2))))
        # Revisar si se llegó al objetivo
        if np.linalg.norm(p2 - actual.objective.vector()) < 0.01:
            actual.objetivo_alcanzado = True

        ## Actualizar variables globales ----------------------------------------------------------------------------
        ## Valores medios
        w1 = (q1 - q1_prev)/2 / deltaT
        w2 = (q2 - q2_prev)/2 / deltaT
        a1_instantaneo = (w1 - w1_prev)/2 / deltaT
        a2_instantaneo = (w2 - w2_prev)/2 / deltaT
        ## Correjir casos extraños donde la pendiente es extremadamente grande
        if abs(w1) > 100:
            w1 = w1_prev
        if abs(w2) > 100:
            w2 = w2_prev
        if abs(a1_instantaneo) > 100:
            a1_instantaneo = w1_dot_prev
        if abs(a2_instantaneo) > 100:
            a2_instantaneo = w2_dot_prev
        
    else:
        ## Reiniciar valores del brazo
        brazo.reiniciar()
        ## Actualizar variables globales ----------------------------------------------------------------------------
        a1_instantaneo = a1_0
        a2_instantaneo = a2_0
        ## Recuperar los valores iniciales en un segundo
        w1, w2 = alcanzar_velocidad(w1_prev, w2_prev)
        q1 = q1_prev + w1*deltaT
        q2 = q2_prev + w2*deltaT
        p1 = R(w1*deltaT).dot(p1_prev)
        p2 = R(w1*deltaT + w2*deltaT).dot(p2_prev - p1_prev) + p1
    
    ## Actualizar vectores velocidad ----------------------------------------------------------------------------    
    v1 = R(q1).dot(np.array([0, l1*rad(w1)]))
    v2_F2 = np.array([-np.sin(rad(q2))*l1*rad(w1), np.cos(rad(q2))*l1*rad(w1) + l2*rad(w1 + w2)])
    v2 = R(q1 + q2).dot(v2_F2)
    ## Actualizar vectores aceleración --------------------------------------------------------------------------    
    a1 = R(q1).dot(np.array([-l1*rad(w1)**2, l1*rad(a1_instantaneo)]))
    a2_F2 = np.array([l1*np.sin(rad(q2))*rad(a1_instantaneo) - l1*np.cos(rad(q2))*(2*rad(w1)**2 + rad(w1)*rad(w2)) - l2*rad(w1 + w2)**2, 
                       l1*np.cos(rad(q2))*rad(a1_instantaneo) + l1*np.sin(rad(q2))*(2*rad(w1)**2 + rad(w1)*rad(w2)) + l2*rad(a1_instantaneo + a2_instantaneo)])
    a2 = R(q1 + q2).dot(a2_F2)
    
    ## Reducir Ángulos
    # np.rad2deg(reducir(np.deg2rad((q1, q2))))
    return (p1, p2), (q1, q2), (w1, w2), (a1_instantaneo, a2_instantaneo), (v1, v2), (a1, a2)

def start():
    brazo.reiniciar()
    data = list()   # Esta será la lista que se rellene con los estados del brazo entre el primer 
                    # y segundo punto seleccionados tras haber iniciado el programa
    punto_encontrado = False  # Solo puede recolectarse data de una linea; punto_encontrado será True cuando
                              # haya un primer punto al que el brazo se dirija y este tenga un objetivo
                              # Es decir, la primera linea dibujada
    observando = None
    # Para evitar grandes cantidades de recursión, se implementará el programa desde acá.
    P_aux, Q_aux, W_aux, W_dot_aux, V_aux, A_aux = main(P_0, Q_0, W_0, (0, 0), V_0, A_0)
    t = 0
    t_0 = 0
    while True:
        P_aux, Q_aux, W_aux, W_dot_aux, V_aux, A_aux = main(P_aux, Q_aux, W_aux, W_dot_aux, V_aux, A_aux)
        # Revisar si contar data o no (solo se cuenta cuando se encontró el primer punto y no se ha llegado al segundo)
        # Esta estructura permite que al dibujar otra linea, el programa genere otro set de datos
        if punto_encontrado:
            try:
                ready = observando.objetivo_alcanzado
            except AttributeError:
                continue
            else:
                if not ready:
                    # Para redirigir el desfase y centrarce en t = 0, se enviará t - t_0 - deltaT
                    # donde t_0 es el momento en que se comenzó a recorrer la linea y delta T el desfase del loop
                    data = agregar_estado(data, t - t_0 - deltaT, np.deg2rad(Q_aux), np.deg2rad(W_aux), np.deg2rad(W_dot_aux), V_aux[1], A_aux[1])
                # Terminó de recorrer la linea
                else:
                    ## Limpiar data para la siguiente linea
                    punto_encontrado = False
                    exportar(data)
                    data.clear()
                    observando = observando.objective

        else:
            # Existe primer punto
            if observando != None:
                # Este primer punto tiene un objetivo
                if observando.objective != None:
                    if not observando.objetivo_alcanzado:
                        t_0 = t
                        punto_encontrado = True
        # Actualizar lo que se observará al poner el primer punto
        if brazo.objective != None and (observando == None):
            observando = brazo.objective
        # Limpieza de memoria
        if brazo.objective == None:
            observando = None

        sleep(deltaT)
        t += deltaT

if __name__ == '__main__':
    # Constantes --------------------------------------------------------------
    # Ángulos en degrees (X°)
    a1_0 = 0
    a2_0 = 0
    w1_0 = 20
    w2_0 = 45
    q1_0 = 0
    q2_0 = 0
    deltaT = 0.01
    l1 = 0.6
    l2 = 0.4
    # Valores iniciales -------------------------------------------------------
    P_0 = (R(q1_0).dot(np.array([l1, 0])), R(q1_0 + q2_0).dot(np.array([l2, 0])) + R(q1_0).dot(np.array([l1, 0])))
    Q_0 = (q1_0, q2_0)
    W_0 = (w1_0, w2_0)
    V_0 = (np.array([0, 0]), np.array([0, 0]))
    A_0 = (np.array([0, 0]), np.array([0, 0]))
    brazo = Punto(arreglo(np.array([l1 + l2, 0])))
    # -------------------------------------------------------------------------
    start()