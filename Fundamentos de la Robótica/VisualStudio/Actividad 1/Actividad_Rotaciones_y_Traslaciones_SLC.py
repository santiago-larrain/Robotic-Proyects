# Pregunta 7
# Autor: Santiago Larraín C.
# Referencias: Código fuente --> draw_line.py
# Dibuja dos planos cartesianos con las rectas que representan los vectores pedidos en la actividad.
# Para las rotaciones de los vectores se utilizó Wolfram Mathematica, facilitando el producto matriz-vector y entregando valores más exactos.

# Program flow
# - Initialize Pygame
# - Create points/vectors as tuples and arrays
# - Draw line

# --- Import basic libraries ---
from cmath import sqrt
import numpy as np  # Load all basic math and array/matrix handling functionality 
import pygame       # Load pygame for IO-interfacing 
                    # (keyboard, mouse, joystick, screen, audio)

# --- Initialize pygame ---
XMAX = 640      # Define the window's width
YMAX = 480      # Define the window's height
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


 
def main():
    
    # Fill the screen with a dark blue color to use it as background color.
    screen.fill((0,0,63))

    # --- Draw rotated objects and some other stuff ---
    ## Initial vectors:
    C1 = np.array([160, 240])
    C2 = np.array([480, 240])
    centros = [C1, C2]
    V = np.array([1,3])*30
    V2_R = np.array([-0.633975, 3.09808])*30
    V2_R_T = np.array([1.36603, 4.09808])*30
    V4_T = np.array([3,4])*30
    V4_T_R_2 = np.array([0.598076, 4.9641])*30
    V4_T_R_1 = np.array([1.23205, 1.86603])*30
    ## Dibujar planos cartesianos:
    for p in range(2):
        # Pregunta:
        font = pygame.font.SysFont('Arial', 20)
        screen.blit(font.render(f"P{p + 1}", True, (200,200,200)), centros[p] + np.array([-10, -180]))
        # Ejes X, Y:
        pygame.draw.line(screen, (200,200,200), centros[p] + np.array([0, 150]), centros[p] + np.array([0, -150]), 1)
        pygame.draw.line(screen, (200,200,200), centros[p] + np.array([-150, 0]), centros[p] + np.array([150, 0]), 1)
        # Malla que marca la unidad:
        for i in range(9):
            if i == 4:
                continue
            pygame.draw.line(screen, (100,100,100), centros[p] + np.array([-150, 30*(i - 4)]), centros[p] + np.array([150, 30*(i-4)]), 1)
            pygame.draw.line(screen, (100,100,100), centros[p] + np.array([30*(i - 4), 150]), centros[p] + np.array([30*(i - 4), -150]), 1)
    
    # P2:
    pygame.draw.line(screen, (255,0,0), C1, C1 + V*np.array([1,-1]), 2)  ## Ojo que hay que ajustar la coordenada Y.
    pygame.draw.line(screen, (0,255,0), C1, C1 + V2_R * np.array([1,-1]), 2)
    pygame.draw.line(screen, (0,0,255), C1 + np.array([2,-1])*30, C1 + V2_R_T*np.array([1,-1]), 2)

    # P4:
    pygame.draw.line(screen, (255,0,0), C2, C2 + V*np.array([1,-1]), 2)  ## Ojo que hay que ajustar la coordenada Y.
    pygame.draw.line(screen, (0,255,0), C2 + np.array([2,-1])*30, C2 + V4_T*np.array([1,-1]), 2)
    pygame.draw.line(screen, (0,0,255), C2 + V4_T_R_1 * np.array([1,-1]), C2 + V4_T_R_2 * np.array([1,-1]), 2)
        
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
                main() # reset the program by execute the program again
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                font = pygame.font.SysFont('Arial', 25)
                text_str = str(mouse_pos)
                screen.blit(font.render(text_str, True, (255,0,0)), mouse_pos)
                pygame.display.flip()
 
if __name__ == '__main__': main()