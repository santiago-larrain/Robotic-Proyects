import numpy as np
import pygame       # Load pygame for IO-interfacing 
import json
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "Simulador/display_parameters.json"

class Display(QObject):

    keyboard_signal = pyqtSignal(str)
    end_signal = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app

        # --- Initialize pygame ---
        self.XMAX = self.p("WINDOW_WIDTH")      # Define the window's width
        self.YMAX = self.p("WINDOW_LENGHT")      # Define the window's height
        self.origen = np.array([self.XMAX/2, self.YMAX/2])
        self.scale = self.p("SCALE")
        
        self.cars = []  # Lista de robots a dibujar
        self.ball = None
        self.arcs = []
        self.texts = []  # Lista de tuplas (texto, ID, *side)

        self.screen = None
        self.key_pressed = None

        self.active = False
        self.thread = threading.Thread(target= self.flip, daemon= False)

    def flip(self):
        pygame.init()   # Start pygame
        self.screen = pygame.display.set_mode((self.XMAX, self.YMAX))   # Display the window
        pygame.display.set_caption(self.p("WINDOW_NAME"))   # Set the window's title
        
        self.active = True
        while self.active:
            start = time.time()
            self.revisar_eventos()
            
            # Inizialize main screen
            self.initialize_screen()

            self.show_texts()      # Texts and different data
            self.draw_objects()    # Cars, balls, arcs...
            
            pygame.display.flip()  # Flip page

            sleep = max(1/self.p("FPS") - (time.time() - start), 0)
            time.sleep(sleep)
        
        pygame.quit()
        self.app.exit()

    def revisar_eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUITis sent when the user clicks the window's "X" button, or when the system 'asks' for the process to quit
                self.active = False
                self.end_signal.emit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.active = False
                self.end_signal.emit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.keyboard_signal.emit("w")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.keyboard_signal.emit("a")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.keyboard_signal.emit("s")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.keyboard_signal.emit("d")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.keyboard_signal.emit("stop")


    def show_texts(self):
        font = pygame.font.SysFont('Arial', 25)
        for text_tuple in self.texts:
            text_str, ID, side = text_tuple
            if side:
                self.screen.blit(font.render(text_str, True, (255,255,255)), (self.XMAX - len(text_str)*11, 10 + ID*35))
            else:
                self.screen.blit(font.render(text_str, True, (255,255,255)), (10, 10 + ID*35))
    
    def initialize_screen(self):
        # Fill the screen with a dark blue color to use it as background color.
        self.screen.fill((0,0,63))
        ## Dibujar plano cartesiano:
        pygame.draw.line(self.screen, (200,200,200), np.array([self.XMAX/2, 10]), np.array([self.XMAX/2, self.YMAX - 10]), 1)
        pygame.draw.line(self.screen, (200,200,200), np.array([10, self.YMAX/2]), np.array([self.XMAX - 10, self.YMAX/2]), 1)
        # Malla que marca la unidad:
        for i in range(self.YMAX//(self.scale//10) + 1):
            if i == self.YMAX//(2*self.scale//10):
                continue
            pygame.draw.line(self.screen, (100,100,100), np.array([10, self.YMAX/2 + (self.scale//10)*(i - self.YMAX//(2*self.scale//10))]),
                                                         np.array([self.XMAX - 10, self.YMAX/2 + (self.scale//10)*(i - self.YMAX//(2*self.scale//10))]), 1)
        for i in range(self.XMAX//(self.scale//10) + 1):
            if i == self.XMAX//(2*self.scale//10):
                continue
            pygame.draw.line(self.screen, (100,100,100), np.array([self.XMAX/2 + (self.scale//10)*(i - self.XMAX//(2*self.scale//10)), 10]),
                                                         np.array([self.XMAX/2 + (self.scale//10)*(i - self.XMAX//(2*self.scale//10)), self.YMAX - 10]), 1)
        
    def draw_objects(self):
        # draw cars
        for car in self.cars:
            car.move(1/self.p("FPS"))
            chassis, wheel_L, wheel_R = self.dimensions(car)
            pygame.draw.polygon(self.screen, tuple(self.p("CAR_CHASSIS_COLOR_1")), chassis, 0)
            pygame.draw.polygon(self.screen, tuple(self.p("CAR_WHEEL_COLOR")), wheel_L, 0)
            pygame.draw.polygon(self.screen, tuple(self.p("CAR_WHEEL_COLOR")), wheel_R, 0)
            #pygame.draw.polygon(self.screen, tuple(self.p("CAR_PALLET_COLOR")), corners["PALLET_1"], 0)
            #pygame.draw.polygon(self.screen, tuple(self.p("CAR_PALLET_COLOR")), corners["PALLET_2"], 0)
            #pygame.draw.polygon(self.screen, tuple(self.p("CAR_PALLET_COLOR")), corners["PALLET_3"], 0)
        
        if self.ball:
            pygame.draw.circle(self.screen, tuple(self.p("BALL_COLOR")), self.ball.pos, self.p("SCALE")*self.p("BALL_RADIOUS"), 0)
        
    def dimensions(self, car):
        CR = car.center_of_rotation()
        director = car.front - car.back
        director = np.array([director[0], -director[1]])
        chassis = [self.display_car(CR, director, [(1 - car.p("gamma_2"))*car.p("CAR_LENGHT"), car.p("CAR_WIDTH")/2]),
                   self.display_car(CR, director, [(1 - car.p("gamma_2"))*car.p("CAR_LENGHT"), - car.p("CAR_WIDTH")/2]),
                   self.display_car(CR, director, [- car.p("gamma_2")*car.p("CAR_LENGHT"), - car.p("CAR_WIDTH")/2]),
                   self.display_car(CR, director, [- car.p("gamma_2")*car.p("CAR_LENGHT"), car.p("CAR_WIDTH")/2])]
        wheels_L = [self.display_car(CR, director, [car.p("WHEEL_LENGHT")/2, car.p("CAR_WIDTH")/2 + car.p("WHEEL_WIDTH")]),
                    self.display_car(CR, director, [car.p("WHEEL_LENGHT")/2, car.p("CAR_WIDTH")/2]),
                    self.display_car(CR, director, [- car.p("WHEEL_LENGHT")/2, car.p("CAR_WIDTH")/2]),
                    self.display_car(CR, director, [- car.p("WHEEL_LENGHT")/2, car.p("CAR_WIDTH")/2 + car.p("WHEEL_WIDTH")])]
        wheels_R = [self.display_car(CR, director, [car.p("WHEEL_LENGHT")/2, - car.p("CAR_WIDTH")/2 - car.p("WHEEL_WIDTH")]),
                    self.display_car(CR, director, [car.p("WHEEL_LENGHT")/2, - car.p("CAR_WIDTH")/2]),
                    self.display_car(CR, director, [- car.p("WHEEL_LENGHT")/2, - car.p("CAR_WIDTH")/2]),
                    self.display_car(CR, director, [- car.p("WHEEL_LENGHT")/2, - car.p("CAR_WIDTH")/2 - car.p("WHEEL_WIDTH")])]
        return chassis, wheels_L, wheels_R
    
    def R(self, t):
        # Matriz de rotación para un ángulo t en radianes.
        return np.array([[np.cos(t), -np.sin(t)], 
                        [np.sin(t), np.cos(t)]])
                    
    def angle(self, v1, v2):
        # Producto punto y cruz
        sin = np.cross(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
        cos = v1.dot(v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
        if sin >= 0 and cos >= 0:
            return np.arcsin(sin)
        elif sin >= 0 and cos < 0:
            return np.pi - np.arccos(-cos)
        elif sin < 0 and cos < 0:
            return np.arccos(-cos) - np.pi
        elif sin < 0 and cos >= 0:
            return np.arcsin(sin)
        return 0
                    
    def display_car(self, CR, director, vector):
        vector = self.R(self.angle(np.array([1,0]), director)).dot(vector)
        return CR + np.array([int(vector[0]*self.p("SCALE")), -int(vector[1]*self.p("SCALE"))])
    
    def p(self, parameter):
        with open(P_ROUTE, "r") as file:
            data = json.load(file)
            try:
                return data[parameter]
            except KeyError:
                print(f"\033[1mWARNING:\033[0m There is no parameter called \033[1m{parameter}\033[0m")
                return None

