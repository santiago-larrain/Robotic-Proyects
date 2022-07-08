#------------------------------------------------------------------------------#
# Keyboard Input Using PyGame
# execute typing: python random_number.py
# http://stackoverflow.com/questions/16044229/how-to-get-keyboard-input-in-pygame
# http://www.pygame.org/docs/ref/key.html
# http://www.tutorialspoint.com/python/python_numbers.htm
# https://docs.python.org/3/library/functions.html#int

# Program flow
# - Initialize state
# - Read user inputs
# - Step model
# - Draw stuff

import sys  # find ouf constants in sys.float_info
            # https://docs.python.org/2/library/sys.html#sys.float%5Finfo

import pygame
from pygame.locals import * # Must include this line to get the OpenGL
                            # definition otherwise importing just PyGame 
                            # is fine.

#import numpy as np
from numpy import *

import time


# State
L = 10 # List length
N = 33  # Maximum number = number of students-1
x = rint(round_(1+N*random.rand(L,1))) # Store a list of L integer random numbers U~[1,N+1] 
k = 0 # Number pointer



# --- Graphics Variables ---
XMAX = 640
YMAX = 480
screen = None

def reset_data():
    global x, k
    
    x = rint(round_(1+N*random.rand(L,1)))
    k = 0       # Number pointer


def update_display():
    global x, k
    
    #x_str = 'x = ' + str(x[k,0])
    x_str = 'x = {:02d}'.format(int(x[k,0])) #https://docs.python.org/3/library/stdtypes.html
    
    pygame.draw.rect(screen, (0,0,0) , screen.get_rect(), 0)
    #level_rnd = int(round(level,0))
    #level_rnd = int(round((YMAX/2)*(level-TL_LO)/(TL_HI-TL_LO),0))
    progress = rint(k/(L-1)*XMAX)
    pygame.draw.rect(screen, (63,63,0) , pygame.Rect(0,YMAX/4,progress,YMAX/2), 0)
    #print screen.get_rect()
    font = pygame.font.SysFont('Arial', 125)
    screen.blit(font.render(x_str, True, (255,255,0)), (180, (YMAX-150)/2))
    pygame.display.flip()


def update_state():
    global k, L
    
    k = k+1
    if (k==L):
        k=L-1
    
    time.sleep(0.5)

 
    
def handle_keyboard():
    global time_scaling, auto, mv_user, ref
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                                       # http://stackoverflow.com/questions/10080715/pygame-event-event-type-pygame-quit-confusion
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit(); #sys.exit() if sys is imported
        if event.type == pygame.KEYDOWN:    # http://www.pygame.org/docs/ref/key.html
            #if    event.key == pygame.K_UP \
            #   or event.key == pygame.K_DOWN:
            #    keyboard_logic(event.key)
            if event.key == pygame.K_r:
                print("\nRunning random number generator!")    
                reset_data()
    return True

def init_display():
    global XMAX, YMAX, screen
    
    # Initialize PyGame and setup a PyGame display
    pygame.init()
    # pygame.display.set_mode()
    screen = pygame.display.set_mode((XMAX,YMAX))
    pygame.display.set_caption('Random Number')
    pygame.key.set_repeat(1,50)     # Works with essentially no delay.
    #pygame.key.set_repeat(0,50)    # Doesn't work because when the delay
                                    # is set to zero, key.set_repeat is
                                    # returned to the default, disabled
                                    # state.
    
def main():
    global XMAX, YMAX, screen
    
    init_display()
    
    while True:

        handle_keyboard()
        update_state()
        update_display()

        #pygame.time.wait(10) # Set a wait-time to delay capture from keyboard to 10 miliseconds
                             # For very fast processes, it may be necessary to slow down the keyboard 
                             # capture rate in order to reduce fast/abrubpt responses. However, beware
                             # that this delay also reduces the sampling time of the simulator.
                             # Without this delay, the sampling time is on average 8 ms, with the
                             # 10 ms delay, the sampling time increase to 18 ms.
                
if __name__ == '__main__': main()