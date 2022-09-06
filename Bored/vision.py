import numpy as np
import cv2
import json
import time
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "parameters/vision_parameters.json"

class Vision(QObject):

	keyboard_signal = pyqtSignal(int)
	
	def __init__(self, nCam= 0, app= None):
		super().__init__()
		self.app = app

		# Inicializar cámara
		self.cap = cv2.VideoCapture(nCam, cv2.CAP_DSHOW) #
		# self.cap.set(cv2.CAP_PROP_SETTINGS, 1)
		self.active = True  # Parámetro bajo el cual el Thread corre
		self.thread = Thread(target= self.thread_ver, daemon= False)

		# Rango de error y colores predeterminados
		self.rango = np.array(self.p("RANGE"))
		self.color = [None]*5 # Colors for car, ball and enemy car
		self.enemy = False
		self.center = np.array([320, 240])
		
		# Valores para controlador
		self.alpha = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.angle_enemy = 0
		self.dist_pix_enemy = 0
		self.dist_mts_enemy = 0

		# variables obtenidas del visualizador (cámara o simulador)
		self.frames = [None]*3 # Frames[0], Frame2, frames[2]
		self.friendly_car = [None]*2 # p1, p2
		self.ball = None	# p3
		self.enemy_car = [None]*2	 # p4, p5
		self.arcs = [None]*2		 # a1, a2
		self.objective = None

		# Otras variables
		self.count = 0		# Contador para ir cambiando los colores a utilizar

	def thread_ver(self):
		# Instanciar ventanas
		cv2.namedWindow(self.p("MAIN_WINDOW"))
		cv2.moveWindow(self.p("MAIN_WINDOW"), self.p("MW_X"), self.p("MW_Y"))
		cv2.namedWindow(self.p("PROGRAM_WINDOW"))
		cv2.moveWindow(self.p("PROGRAM_WINDOW"), self.p("PW_X"), self.p("PW_Y"))
		
		while self.active:
			start = time.time()
			ret, self.frames[0] = self.cap.read() #
			
			self.frames[1] = cv2.cvtColor(self.frames[0], cv2.COLOR_BGR2HSV)

			self.color_masks = [self.filtro(self.color[0]),
								self.filtro(self.color[1]),
								self.filtro(self.color[2]),
								self.filtro(self.color[3]),
								self.filtro(self.color[4])]
			
			## --- Matemáticas --- ##
			self.mask()    # Calcular matrices de colores y combinarlas con la  original para tener la filtrada
			self.math()   # 

			## --- Mostrar en ventana --- ##
			self.mostrar(f"Angle: {round(np.degrees(self.alpha), 1)} deg", 1)
			self.mostrar(f"Distance: {round(self.dist_mts, 2)} cm", 2)
			
			## --- Mostrar pantallas y revisar evento de mouse --- ##
			cv2.imshow(self.p("PROGRAM_WINDOW"), cv2.resize(self.frames[2], (960, 720)))
			cv2.imshow(self.p("MAIN_WINDOW"), cv2.resize(self.frames[0], (960, 720)))
			cv2.setMouseCallback(self.p("MAIN_WINDOW"), self.click_event)
			
			## --- Revisar inputs y emitir estado --- ##
			self.keyboard()
			
			time.sleep(max(self.p("SLEEP") - (time.time() - start), 0))
		
		self.cap.release()
		cv2.destroyAllWindows()


	## ---------- Funciones para ajustar y realizar tareas pequeñas y repetitivas ---------- ##

	def filtro(self, col):
		# Devuelve las matrices de frames que solo contiene al color pedido con cierto rango de error
		if col is None:
			# Defoult: Rosado brillante y saturado
			return cv2.inRange(self.frames[1], np.array(self.p("DEFAULT_COLOR")) - np.array([0,0,1]), np.array(self.p("DEFAULT_COLOR")))
		return cv2.inRange(self.frames[1], col - self.rango, col + self.rango)

	def mostrar(self, txt, ID, *rght):
		col = 10
		if rght:
			col = 450
		cv2.putText(self.frames[2], str(txt), (col, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
		
	def angle(self, v1, v2):
		# Ángulo entre dos vectores alpha -> [-Pi, Pi]
		sin = np.cross(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
		cos = v1.dot(v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
		if cos >= 0:
			return np.arcsin(sin)
		elif cos < 0:
			return np.sign(sin)*np.arccos(cos)
		else:
			return 0
	
	def int_array(self, vector):
		# Pasa un vector a ints para poder trabajarlo en las frames
		return np.array([int(vector[0]), int(vector[1])])

	## ---------- Funciones de matemáticas y máscara: Tareas más complejas e importantes ---------- ##
		
	def math(self):
		if str(self.friendly_car) != str([None, None]) and str(self.objective) != "None":
			# Función para determinar ángulo y distancia a objetivo
			(x1, y1), (x2, y2) = self.friendly_car
			(x3, y3) = self.objective
			
			# Vectores
			vector_12 = np.array([x2 - x1, -(y2 - y1)])
			vector_13 = np.array([x3 - x1, -(y3 - y1)])

			# Establecer ángulo = [-180°, 180°]
			self.alpha = self.angle(vector_12, vector_13)
			# Distancia en pixeles
			self.dist_pix = np.linalg.norm(vector_13)
			# Distancia en metros
			self.dist_mts = self.p("LARGO_AUTO")*np.linalg.norm(vector_13)/np.linalg.norm(vector_12)
			if str(self.dist_mts) == "nan" or str(self.dist_mts) == "inf":
				self.dist_mts = 0
		
		# Lo mismo, pero para el enemigo
		if str(self.enemy_car) != str([None, None]) and str(self.ball) != "None":
			# Función para determinar ángulo y distancia a objetivo
			(x1, y1), (x2, y2) = self.enemy_car
			(x3, y3) = self.objective
			

			# Vectores
			vector_12 = np.array([x2 - x1, -(y2 - y1)])
			vector_13 = np.array([x3 - x1, -(y3 - y1)])

			# Establecer ángulo = [-180°, 180°]
			self.angle_enemy = self.angle(vector_12, vector_13)
			# Distancia en pixeles
			self.dist_pix_enemy = np.linalg.norm(vector_13)
			# Distancia en metros
			self.dist_mts_enemy = self.p("LARGO_AUTO")*np.linalg.norm(vector_13)/np.linalg.norm(vector_12)
			if str(self.dist_mts_enemy) == "nan" or str(self.dist_mts_enemy) == "inf":
				self.dist_mts_enemy = 0

	def mask(self):
		# Variable para saber qué filtros se tienen
		points = 0
		for p, c in zip(range(5), self.color_masks):
			try:
				ret, thresh = cv2.threshold(c, 127, 255, 0)
				M = cv2.moments(thresh)
				X = int(M["m10"] / M["m00"])
				Y = int(M["m01"] / M["m00"])
				cv2.circle(self.frames[0], (X, Y), 5, (255, 255, 255), -1)
			except ZeroDivisionError or NameError:
				if p <= 1:
					self.frames[2] = self.frames[0].copy()
				break
			else:
				if p == 0:
					self.friendly_car[0] = np.array([X, Y])
					points += 1
				elif p == 1:
					self.friendly_car[1] = np.array([X, Y])
					mask = cv2.bitwise_or(self.color_masks[0], self.color_masks[1])
					points += 1
				elif p == 2:
					self.ball = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.color_masks[2])
					points += 1
				elif p == 3:
					self.enemy_car[0] = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.color_masks[3])
					points += 1
				elif p == 4:
					self.enemy_car[1] = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.color_masks[4])
					points += 1
		
		if points >= 2:
			# Está el auto completo

			self.frames[2] = cv2.bitwise_and(self.frames[0], self.frames[0], mask= mask)

			# --- DIBUJAR ---
			# Linea del auto
			cv2.line(self.frames[2], self.friendly_car[0], self.friendly_car[1], (255, 255, 255), 3)
			
			if str(self.objective) != "None":
				# Linea entre base del auto y objetivo
				cv2.line(self.frames[2], self.friendly_car[0], self.objective, (255, 255, 255), 3)
			if points == 5:
				# Linea del auto enemigo
				cv2.line(self.frames[2], self.enemy_car, self.enemy_car, (125, 125, 125), 3)

		# Mostrar arcos
		arc = 0
		if str(self.arcs[0]) != "None":
			cv2.circle(self.frames[0], self.arcs[0], 5, (255, 100, 100), -1)
			cv2.circle(self.frames[2], self.arcs[0], 5, (255, 100, 100), -1)
			arc += 1
		if str(self.arcs[1]) != "None":
			cv2.circle(self.frames[0], self.arcs[1], 5, (100, 100, 255), -1)
			cv2.circle(self.frames[2], self.arcs[1], 5, (100, 100, 255), -1)
			arc += 1
		# Marcar centro
		if arc == 2:
			self.center = self.int_array(self.arcs[0]/2 + self.arcs[1]/2)
			cv2.circle(self.frames[0], self.center, 3, (100, 255, 100), -1)
			cv2.circle(self.frames[2], self.center, 3, (100, 255, 100), -1)

	## ---------- Mouse and Keyboard readers ---------- ##

	def click_event(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			selected_color = self.frames[1][y][x]
			if not self.enemy:
				if self.count in [3, 4]:
					self.count = 5
			if self.count == 0:
				self.color[0] = selected_color
			if self.count == 1:
				self.color[1] = selected_color
			if self.count == 2:
				self.color[2] = selected_color
			if self.count == 3:
				self.color[3] = selected_color
			if self.count == 4:
				self.color[4] = selected_color
			if self.count == 5:
				self.arcs[0] = np.array([x, y])
			if self.count == 6:
				self.arcs[1] = np.array([x, y])

			self.count += 1
			if self.count == 7:
				# The las clicks are always for the arcs
				self.count = 5
		
		if event == cv2.EVENT_RBUTTONDOWN:
			self.color = [None]*5
			self.arcs = [None]*2
			self.center = np.array([320, 240])
			self.count = 0
	
	def keyboard(self):
		# Leer comandos del teclado y emitirlos a los HQ
		key = cv2.waitKey(1)
		if key != -1:
			self.keyboard_signal.emit(key)

	def restart(self):
		# Restore initial values for variables

		self.color = [None]*5 # Colors for car, ball and enemy car
		self.enemy = False
		self.center = np.array([320, 240])

		# Valores para controlador
		self.alpha = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.angle_enemy = 0
		self.dist_pix_enemy = 0
		self.dist_mts_enemy = 0

		# variables obtenidas del visualizador (cámara o simulador)
		self.frames = [None]*3 # Frames[0], Frame2, frames[2]
		self.friendly_car = [None]*2 # p1, p2
		self.ball = None	# p3
		self.enemy_car = [None]*2	 # p4, p5
		self.arcs = [None]*2		 # a1, a2
		self.objective = None

		# Otras variables
		self.count = 0		# Contador para ir cambiando los colores a utilizar

	def end(self):
		self.active = False
		try:
			self.thread.join()
		except RuntimeError:
			pass
		self.app.exit()

	# Leer parámetros
	def p(self, parameter):
		with open(P_ROUTE, "r") as file:
			data = json.load(file)
			try:
				return data[parameter]
			except KeyError:
				print(f"\033[1mWARNING: [Vision]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
				return None
