import numpy as np
from time import sleep
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)


# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
size_line = 6
scale_line = 200

pygame.init()   # Start pygame
# pygame.display.set_mode()
screen = pygame.display.set_mode((XMAX,YMAX))   # Display the window.
                                                # This creates a so-called
                                                # 'drawing surface' or simply
                                                # 'Surface'.
pygame.display.set_caption('Draw Line')   # Set the window's title
pygame.key.set_repeat(1,50)  # Works with essentially no delay, i.e.
                            # keeping a key pressed generates a continuous
                            # sequence of inputs and does not require the
                            # the user to release the keyboard to input
                            # characters as a repetition of key strokes.
#pygame.key.set_repeat(0,50) # Doesn't work because when the delay is set to
                            # zero, key.set_repeat is returned to the default,
                            # disabled state

def R(t):
    theta = t*np.pi/180
    return np.array([[np.cos(theta), -np.sin(theta)], 
                     [np.sin(theta), np.cos(theta)]])
                
def rotar_ex(l1, l2, a1, a2):
    P2_rotado = R(a1 + a2).dot(l2)
    P1_rotado = R(a1).dot(l1)
    P2_rotado_trasladado = P2_rotado + P1_rotado
    return P1_rotado, P2_rotado_trasladado


def main(p1_prev, p2_prev,q1_prev, q2_prev, w1_prev, w2_prev, v1a_prev, v2a_prev, v1b_prev, v2b_prev):

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
    
    def arreglo(l):
        lx, ly = l
        return np.array([lx, -ly])*scale_line + np.array([XMAX/2, YMAX/2])

    pygame.draw.line(screen, (150, 200, 150), arreglo((0,0)), arreglo(p1_prev), size_line)
    pygame.draw.line(screen, (200, 150, 200), arreglo(p1_prev), arreglo(p2_prev), size_line)
    
    # Vector velocidad P y sus componentes en base local:
    def a():
        # P1
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1a_prev + p1_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p1_prev), arreglo(np.array([v1a_prev[0], 0]) + p1_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v1a_prev[0], 0]) + p1_prev), arreglo(v1a_prev + p1_prev), size_line//2)
        # P2
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2a_prev + p2_prev), size_line)
        pygame.draw.line(screen, (150, 0, 0), arreglo(p2_prev), arreglo(np.array([v2a_prev[0], 0]) + p2_prev), size_line//2)
        pygame.draw.line(screen, (150, 0, 0), arreglo(np.array([v2a_prev[0], 0]) + p2_prev), arreglo(v2a_prev + p2_prev), size_line//2)
        
        # Local proyection --------------
        # P1
        v1a_proyectado = R(-q1_prev).dot(v1a_prev)
        v1a_x = v1a_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (255, 0, 0), arreglo(p1_prev), arreglo(v1a_x + p1_prev), size_line//3)
        pygame.draw.line(screen, (255, 0, 0), arreglo(v1a_x + p1_prev), arreglo(v1a_prev + p1_prev), size_line//3)
        # P2
        v2a_proyectado = R(-(q1_prev + q2_prev)).dot(v2a_prev)
        v2a_x = v2a_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (255, 0, 0), arreglo(p2_prev), arreglo(v2a_x + p2_prev), size_line//3)
        pygame.draw.line(screen, (255, 0, 0), arreglo(v2a_x + p2_prev), arreglo(v2a_prev + p2_prev), size_line//3)
        # -----------------------

    def b():
        # P1
        pygame.draw.line(screen, (0, 255, 0), arreglo(p1_prev), arreglo(v1b_prev + p1_prev), size_line)
        pygame.draw.line(screen, (0, 150, 0), arreglo(p1_prev), arreglo(np.array([v1b_prev[0], 0]) + p1_prev), size_line//3)
        pygame.draw.line(screen, (0, 150, 0), arreglo(np.array([v1b_prev[0], 0]) + p1_prev), arreglo(v1b_prev + p1_prev), size_line//3)
        # P2
        pygame.draw.line(screen, (0, 255, 0), arreglo(p2_prev), arreglo(v2b_prev + p2_prev), size_line)
        pygame.draw.line(screen, (0, 150, 0), arreglo(p2_prev), arreglo(np.array([v2b_prev[0], 0]) + p2_prev), size_line//3)
        pygame.draw.line(screen, (0, 150, 0), arreglo(np.array([v2b_prev[0], 0]) + p2_prev), arreglo(v2b_prev + p2_prev), size_line//3)

        # Local proyection --------------
        # P1
        v1b_proyectado = R(-q1_prev).dot(v1b_prev)
        v1b_x = v1b_proyectado[0] * p1_prev / np.linalg.norm(p1_prev)
        pygame.draw.line(screen, (0, 255, 0), arreglo(p1_prev), arreglo(v1b_x + p1_prev), size_line//3)
        pygame.draw.line(screen, (0, 255, 0), arreglo(v1b_x + p1_prev), arreglo(v1b_prev + p1_prev), size_line//3)
        # P2
        v2b_proyectado = R(-(q1_prev + q2_prev)).dot(v2b_prev)
        v2b_x = v2b_proyectado[0] * (p2_prev - p1_prev) / np.linalg.norm(p2_prev - p1_prev)
        pygame.draw.line(screen, (0, 255, 0), arreglo(p2_prev), arreglo(v2b_x + p2_prev), size_line//3)
        pygame.draw.line(screen, (0, 255, 0), arreglo(v2b_x + p2_prev), arreglo(v2b_prev + p2_prev), size_line//3)
        # -----------------------
    
    ## Elegir a) o b) -------------------------------------------------------------------------------------
    a()
    b()
    ## ----------------------------------------------------------------------------------------------------
    # --- Send graphic buffer to the physical screen to make it appear ---
    # This step is necessary to refrech the screen once the drawing is done.
    pygame.display.flip()
    
    # --- Wait for the user to press ESC, 
    #     click on the window closing icon 'X',
    #     or press a mouse button. ---
    # If a mouse button is pressed, the mouse's position coordinates at
    # the location where it was pressed are obtained and printed on the screen.

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                    #  http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            main(l1_vector, l2_vector, 0, 0, np.array([0,0]), np.array([0,0]), np.array([0,0]), np.array([0,0])) # reset the program by execute the program again
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            font = pygame.font.SysFont('Arial', 25)
            text_str = str(mouse_pos)
            screen.blit(font.render(text_str, True, (255,0,0)), mouse_pos)
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
    v1b = R(q1).dot(np.array([0, l1*(w1/180 * np.pi)]))
    v2b_F2 = np.array([-np.sin(q2/180 * np.pi)*l1*(w1/180 * np.pi), 
                    np.cos(q2/180 * np.pi)*l1*(w1/180 * np.pi) + l2*((w1/180 * np.pi) + (w2/180 * np.pi))])
    v2b = R(q1 + q2).dot(v2b_F2)
    
    return p1, p2, q1, q2, w1, w2, v1a, v2a, v1b, v2b

        

if __name__ == '__main__':
    # Para evitar grandes cantidades de recursión, se implementará el programa desde acá.
    # Constantes --------------------------------------------------------------
    a1 = 0
    a2 = 0
    #w1 = 20
    #w2 = 45
    q1_0 = 0
    q2_0 = 0
    w1_0 = 20
    w2_0 = 45
    deltaT = 0.01
    l1 = 0.6
    l2 = 0.4
    l1_vector = np.array([l1, 0])
    l2_vector = np.array([l2, 0]) + l1_vector
    # -------------------------------------------------------------------------
    p1_aux, p2_aux, q1_aux, q2_aux, w1_aux, w2_aux, v1a_aux, v2a_aux, v1b_aux, v2b_aux = main(l1_vector, l2_vector, q1_0, q2_0, w1_0, w2_0, 
                                                                                            np.array([0, 0]), np.array([0, 0]), np.array([0, 0]), np.array([0, 0]))
    t = 0
    while True:
        sleep(deltaT)
        p1_aux, p2_aux, q1_aux, q2_aux, w1_aux, w2_aux, v1a_aux, v2a_aux, v1b_aux, v2b_aux = main(p1_aux, p2_aux, q1_aux, q2_aux, w1_aux, w2_aux, v1a_aux, v2a_aux, v1b_aux, v2b_aux)
        t += deltaT