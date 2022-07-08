import numpy as np
from time import sleep
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)


# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
scale_line = 200

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

prints = []
def revisar_eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                    #  http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            main() # reset the program by execute the program again
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            font = pygame.font.SysFont('Arial', 25)
            text_str = "°"
            prints.append((font.render(text_str, True, (255,0,0)), mouse_pos))

def arreglo(l):
        lx, ly = l
        return np.array([lx, -ly])*scale_line + np.array([XMAX/2, YMAX/2])

def rad(theta):
    return theta*np.pi/180

def R(t):
    return np.array([[np.cos(rad(t)), -np.sin(rad(t))], 
                     [np.sin(rad(t)), np.cos(rad(t))]])
                
def rotar_ex(l1, l2, a1, a2):
    P2_rotado = R(a1 + a2).dot(l2)
    P1_rotado = R(a1).dot(l1)
    P2_rotado_trasladado = P2_rotado + P1_rotado
    return P1_rotado, P2_rotado_trasladado

def angulos_optimos(p_optimo, l_base, q_inicial):
    ## p_optimo = [p*_x, p*_y]
    ## l_base = (l1, l2)
    ## q_inicial = [q1, q2]

    def J_q(q_0):
        t_1 = q_0[0] * np.pi / 180
        t_2 = q_0[1] * np.pi / 180
        return np.array([[-l1*np.sin(t_1) - l2*np.sin(t_1 + t_2), -l2*np.sin(t_1 + t_2)],
                         [l1*np.cos(t_1) + l2*np.cos(t_1 + t_2), l2*np.cos(t_1 + t_2)]])


    epsilon = 1e-10
    l1, l2 = l_base
    q_viejo = q_inicial
    t1 = q_viejo[0] * np.pi / 180
    t2 = q_viejo[1] * np.pi / 180
    p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])
    #print(f"p: {p_actual}\nq: {q_viejo}\n-------------")

    q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)
    
    while ((p_optimo - p_actual) > epsilon).any() and \
          ((q_nuevo - q_viejo) > epsilon).any():
        
        q_viejo = q_nuevo
        
        t1 = q_viejo[0] * np.pi / 180
        t2 = q_viejo[1] * np.pi / 180
        p_actual = np.array([l1*np.cos(t1) + l2*np.cos(t1 + t2),
                         l1*np.sin(t1) + l2*np.sin(t1 + t2)])
        
        q_nuevo = q_viejo + np.linalg.pinv(J_q(q_viejo)).dot(p_optimo - p_actual)
    
    q_rotar = q_nuevo - q_inicial
    return q_rotar

def main(P, Q, W, Va, Vb, Aa, Ab):
    # Variables -------------
    p1_prev, p2_prev = P
    q1_prev, q2_prev = Q
    w1_prev, w2_prev = W
    v1a_prev, v2a_prev = Va
    v1b_prev, v2b_prev = Vb
    a1a_prev, a2a_prev = Aa
    a1b_prev, a2b_prev = Ab
    # -----------------------

    ####################################################################################
    #### Funciones de dibujo, cada una está encargada de dibujar un tipo de vectores ###
    ####################################################################################
    
    def draw_arms(size_line):
        pygame.draw.line(screen, (200, 200, 200), arreglo((0,0)), arreglo(p1_prev), size_line)
        pygame.draw.line(screen, (150, 150, 150), arreglo(p1_prev), arreglo(p2_prev), size_line)
    
    # Vector velocidad P y sus componentes en base local y global:
    def velocidad_a_global(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1a_prev + p1_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p1_prev), arreglo(np.array([v1a_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v1a_prev[0], 0]) + p1_prev), arreglo(v1a_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2a_prev + p2_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p2_prev), arreglo(np.array([v2a_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v2a_prev[0], 0]) + p2_prev), arreglo(v2a_prev + p2_prev), size_line//2)
        
    def velocidad_a_local(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1a_prev + p1_prev), size_line)
        v1a_proyectado = R(-q1_prev).dot(v1a_prev)
        v1a_x = v1a_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1a_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (255, 0, 0), arreglo(v1a_x + p1_prev), arreglo(v1a_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2a_prev + p2_prev), size_line)
        v2a_proyectado = R(-(q1_prev + q2_prev)).dot(v2a_prev)
        v2a_x = v2a_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2a_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (255, 0, 0), arreglo(v2a_x + p2_prev), arreglo(v2a_prev + p2_prev), size_line//2)
        # -----------------------

    def velocidad_b_global(size_line):
        # P1
        pygame.draw.line(screen, (0, 255, 0), arreglo(p1_prev), arreglo(v1b_prev + p1_prev), size_line)
        pygame.draw.line(screen, (0, 150, 0), arreglo(p1_prev), arreglo(np.array([v1b_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 0), arreglo(np.array([v1b_prev[0], 0]) + p1_prev), arreglo(v1b_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 255, 0), arreglo(p2_prev), arreglo(v2b_prev + p2_prev), size_line)
        pygame.draw.line(screen, (0, 150, 0), arreglo(p2_prev), arreglo(np.array([v2b_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 0), arreglo(np.array([v2b_prev[0], 0]) + p2_prev), arreglo(v2b_prev + p2_prev), size_line//2)

    def velocidad_b_local(size_line):
        # P1
        pygame.draw.line(screen, (0, 255, 0), arreglo(p1_prev), arreglo(v1b_prev + p1_prev), size_line)
        v1b_proyectado = R(-q1_prev).dot(v1b_prev)
        v1b_x = v1b_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (0, 255, 0), arreglo(p1_prev), arreglo(v1b_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 255, 0), arreglo(v1b_x + p1_prev), arreglo(v1b_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 255, 0), arreglo(p2_prev), arreglo(v2b_prev + p2_prev), size_line)
        v2b_proyectado = R(-(q1_prev + q2_prev)).dot(v2b_prev)
        v2b_x = v2b_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (0, 255, 0), arreglo(p2_prev), arreglo(v2b_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 255, 0), arreglo(v2b_x + p2_prev), arreglo(v2b_prev + p2_prev), size_line//2)
        # -----------------------
    
    # Vector aceleración P y sus componentes en base global y local:
    def aceleracion_a_global(size_line):
        # P1
        pygame.draw.line(screen, (0, 255, 255), arreglo(p1_prev), arreglo(a1a_prev + p1_prev), size_line)
        pygame.draw.line(screen, (0, 150, 150), arreglo(p1_prev), arreglo(np.array([a1a_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 150), arreglo(np.array([a1a_prev[0], 0]) + p1_prev), arreglo(a1a_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 255, 255), arreglo(p2_prev), arreglo(a2a_prev + p2_prev), size_line)
        pygame.draw.line(screen, (0, 150, 150), arreglo(p2_prev), arreglo(np.array([a2a_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 150, 150), arreglo(np.array([a2a_prev[0], 0]) + p2_prev), arreglo(a2a_prev + p2_prev), size_line//2)
        
    def aceleracion_a_local(size_line):
        # P1
        pygame.draw.line(screen, (0, 255, 255), arreglo(p1_prev), arreglo(a1a_prev + p1_prev), size_line)
        a1a_proyectado = R(-q1_prev).dot(a1a_prev)
        a1a_x = a1a_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (0, 255, 255), arreglo(p1_prev), arreglo(a1a_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (0, 255, 255), arreglo(a1a_x + p1_prev), arreglo(a1a_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (0, 255, 255), arreglo(p2_prev), arreglo(a2a_prev + p2_prev), size_line)
        a2a_proyectado = R(-(q1_prev + q2_prev)).dot(a2a_prev)
        a2a_x = a2a_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (0, 255, 255), arreglo(p2_prev), arreglo(a2a_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (0, 255, 255), arreglo(a2a_x + p2_prev), arreglo(a2a_prev + p2_prev), size_line//2)
        # -----------------------

    def aceleracion_b_global(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 255), arreglo(p1_prev), arreglo(a1b_prev + p1_prev), size_line)
        pygame.draw.line(screen, (150, 0, 150), arreglo(p1_prev), arreglo(np.array([a1b_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 150), arreglo(np.array([a1b_prev[0], 0]) + p1_prev), arreglo(a1b_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 255), arreglo(p2_prev), arreglo(a2b_prev + p2_prev), size_line)
        pygame.draw.line(screen, (150, 0, 150), arreglo(p2_prev), arreglo(np.array([a2b_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 150), arreglo(np.array([a2b_prev[0], 0]) + p2_prev), arreglo(a2b_prev + p2_prev), size_line//2)

    def aceleracion_b_local(size_line):
        # P1
        pygame.draw.line(screen, (255, 0, 255), arreglo(p1_prev), arreglo(a1b_prev + p1_prev), size_line)
        a1b_proyectado = R(-q1_prev).dot(a1b_prev)
        a1b_x = a1b_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (255, 0, 255), arreglo(p1_prev), arreglo(a1b_x + p1_prev), size_line//2)
        pygame.draw.line(screen, (255, 0, 255), arreglo(a1b_x + p1_prev), arreglo(a1b_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 255), arreglo(p2_prev), arreglo(a2b_prev + p2_prev), size_line)
        a2b_proyectado = R(-(q1_prev + q2_prev)).dot(a2b_prev)
        a2b_x = a2b_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (255, 0, 255), arreglo(p2_prev), arreglo(a2b_x + p2_prev), size_line//2)
        pygame.draw.line(screen, (255, 0, 255), arreglo(a2b_x + p2_prev), arreglo(a2b_prev + p2_prev), size_line//2)
        # -----------------------
    

    ## Inicializar -----------------------------------------------------------------------------------------
    initialize_screen()
    draw_arms(10)
    # Velocidad -----------
    #velocidad_a_global(5)
    #velocidad_a_local(5)
    velocidad_b_global(5)
    velocidad_b_local(5)
    # Aceleración ---------
    #aceleracion_a_global(3)
    #aceleracion_a_local(3)
    aceleracion_b_global(3)
    aceleracion_b_local(3)
    ## -----------------------------------------------------------------------------------------------------
    revisar_eventos()
    for event in prints:
        screen.blit(*event)
    pygame.display.flip()

    
    ## Actualizar variables globales ----------------------------------------------------------------------------
    w1 = w1_prev + a1*deltaT
    w2 = w2_prev + a2*deltaT
    q1 = q1_prev + w1*deltaT
    q2 = q2_prev + w2*deltaT
    
    ## Actualizar vectores posición -----------------------------------------------------------------------------
    p1 = R(w1*deltaT).dot(p1_prev)
    p2 = R(w1*deltaT + w2*deltaT).dot(p2_prev - p1_prev) + p1
    
    ## Actualizar vectores velocidad ----------------------------------------------------------------------------
    v1a = (p1 - p1_prev) / deltaT
    v2a = (p2 - p2_prev) / deltaT
    v1b = R(q1).dot(np.array([0, l1*rad(w1)]))
    v2b_F2 = np.array([-np.sin(rad(q2))*l1*rad(w1), np.cos(rad(q2))*l1*rad(w1) + l2*rad(w1 + w2)])
    v2b = R(q1 + q2).dot(v2b_F2)
    
    ## Actualizar vectores aceleración --------------------------------------------------------------------------
    a1a = (v1a - v1a_prev) / deltaT
    a2a = (v2a - v2a_prev) / deltaT
    a1b = R(q1).dot(np.array([-l1*rad(w1)**2, l1*rad(a1)]))
    a2b_F2 = np.array([l1*np.sin(rad(q2))*rad(a1) - l1*np.cos(rad(q2))*(2*rad(w1)**2 + rad(w1)*rad(w2)) - l2*rad(w1 + w2)**2, 
                       l1*np.cos(rad(q2))*rad(a1) + l1*np.sin(rad(q2))*(2*rad(w1)**2 + rad(w1)*rad(w2)) + l2*rad(a1 + a2)])
    a2b = R(q1 + q2).dot(a2b_F2)
    ## Actualizar vectores aceleración ----------------------------------------------------------------------------
    return (p1, p2), (q1, q2), (w1, w2), (v1a, v2a), (v1b, v2b), (a1a, a2a), (a1b, a2b)

        

if __name__ == '__main__':
    # Para evitar grandes cantidades de recursión, se implementará el programa desde acá.
    # Constantes --------------------------------------------------------------
    # Ángulos en degrees (X°)
    a1 = 10
    a2 = 0
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
    Va_0 = (np.array([0, 0]), np.array([0, 0]))
    Vb_0 = (np.array([0, 0]), np.array([0, 0]))
    Aa_0 = (np.array([0, 0]), np.array([0, 0]))
    Ab_0 = (np.array([0, 0]), np.array([0, 0]))
    # -------------------------------------------------------------------------
    
    P_aux, Q_aux, W_aux, Va_aux, Vb_aux, Aa_aux, Ab_aux = main(P_0, Q_0, W_0, Va_0, Vb_0, Aa_0, Ab_0)
    t = 0
    while True:
        P_aux, Q_aux, W_aux, Va_aux, Vb_aux, Aa_aux, Ab_aux = main(P_aux, Q_aux, W_aux, Va_aux, Vb_aux, Aa_aux, Ab_aux)
        sleep(deltaT)
        t += deltaT