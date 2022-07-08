from tkinter import W
import numpy as np
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)


# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
size_line = 3
scale_line = 200
w = 2

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

def main(l1, l2):
    
    # Fill the screen with a dark blue color to use it as background color.
    screen.fill((0,0,63))
    ## Dibujar plano cartesiano:
    pygame.draw.line(screen, (200,200,200), np.array([XMAX/2, 10]), np.array([XMAX/2, YMAX - 10]), 1)
    pygame.draw.line(screen, (200,200,200), np.array([10, YMAX/2]), np.array([XMAX - 10, YMAX/2]), 1)
    # Malla que marca la unidad:
    for i in range(18):
        if i == 9:
            continue
        pygame.draw.line(screen, (100,100,100), np.array([10, YMAX/2 + 30*(i-9)]), np.array([XMAX - 10, YMAX/2 + 30*(i-9)]), 1)
        pygame.draw.line(screen, (100,100,100), np.array([XMAX/2 + 30*(i-9), 10]), np.array([XMAX/2 + 30*(i-9), YMAX - 10]), 1)
    
    def arreglo(l):
        lx, ly = l
        return np.array([lx, -ly])*scale_line + np.array([XMAX/2, YMAX/2])


    pygame.draw.line(screen, (255, 0, 0), arreglo((0,0)), arreglo(l1), size_line)
    pygame.draw.line(screen, (0, 0, 255), arreglo(l1), arreglo(l2), size_line)

    # --- Send graphic buffer to the physical screen to make it appear ---
    # This step is necessary to refrech the screen once the drawing is done.
    pygame.display.flip()
    
    print('Press ESC to exit...')
    
    # --- Wait for the user to press ESC, 
    #     click on the window closing icon 'X',
    #     or press a mouse button. ---
    # If a mouse button is pressed, the mouse's position coordinates at
    # the location where it was pressed are obtained and printed on the screen.

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                        #  http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
                pygame.quit(); #sys.exit() if sys is imported

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); #sys.exit() if sys is imported
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                l1 = np.array([0.6, 0])
                l2 = np.array([0.4, 0]) + l1
                main(l1, l2) # reset the program by execute the program again
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                L1, L2 = rotar_ex(l1, l2-l1, -w, 0)
                main(L1, L2)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                L1, L2 = rotar_ex(l1, l2-l1, w, 0)
                main(L1, L2)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                L1, L2 = rotar_ex(l1, l2-l1, 0, -w)
                main(L1, L2)
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                L1, L2 = rotar_ex(l1, l2-l1, 0, w)
                main(L1, L2)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                font = pygame.font.SysFont('Arial', 25)
                text_str = str(mouse_pos)
                screen.blit(font.render(text_str, True, (255,0,0)), mouse_pos)
                pygame.display.flip()


if __name__ == '__main__':
    l1 = np.array([0.6, 0])
    l2 = np.array([0.4, 0]) + l1
    main(l1, l2)