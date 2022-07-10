import numpy as np
import cv2
import json
import time
import serial
from threading import Thread

class Coms:

	def __init__(self):
		self.msg = p("MESSAGE").format(motor1= 0, motor2= 0)
		self.active = False
		self.breaked = False
		# seria.Serial nos permite abrir el puerto COM deseado
		self.ser = None
		self.thread = None
		
	def thread_comunicar(self):
		while self.active:
			# El Ambos mensajes que estan en formato Sring deben ser transformados en un arreglo de bytes mediante la funcion .encode
			msgencode = str.encode(self.msg)
			try:
				# .write nos permite enviar el arreglo de bytes correspondientes a los mensajes
				self.ser.write(msgencode)
			except:
				self.breaked = True
				self.active = False
			else:
				time.sleep(p("PERIOD_COMS"))
		
		if not self.breaked:
			# Stop the car
			msgencode = str.encode(p("MESSAGE").format(motor1= 0, motor2= 0))
			self.ser.write(msgencode)
			self.ser.close()
		else:
			self.breaked = False
		print("\033[1mMESSAGE:\033[0m Comunicación por BlueTooth terminada")

	def restart(self):
		self.active = False
		self.breaked = False
		self.ser = None
		self.thread = None

		try:
			# Probar comunicación
			self.ser = serial.Serial(p("COM"), baudrate = p("BR"), timeout = 1)
		except serial.serialutil.SerialException:
			# En caso de error, finalizar comunicación
			print("\033[1mWARNING:\033[0m Fallo de comunicación por BlueTooth")
		else:
			print("\033[1mMESSAGE:\033[0m Comunicación por BlueTooth establecida exitosamente")
			self.active = True
			self.thread = Thread(target= self.thread_comunicar, daemon= False)
			self.thread.start()

		
class Vision:

	def __init__(self, nCam= 0, antena= None):
		self.antena = antena
		self.task = None
		
		# Rango de error y colores predeterminados
		self.rango = np.array(p("RANGE"))
		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.c4 = None
		self.c5 = None
		self.enemy = False
		
		# Inicializar cámara
		self.cap = cv2.VideoCapture(nCam, cv2.CAP_DSHOW) #
		self.cap.set(cv2.CAP_PROP_SETTINGS, 1)
		self.thread = Thread(target= self.thread_ver, daemon= False)

		# Valores para controlador
		self.angle = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.angle_enemy = 0
		self.dist_pix_enemy = 0
		self.dist_mts_enemy = 0
		self.dist_push = 0
		self.motorRPM_1 = 0
		self.motorRPM_2 = 0
		self.car_vel = p("CAR_VEL")

		# Constantes PID
		self.start = 0
		self.pid_period = 0
		self.sgn = 1
		self.k0 = 0
		self.k1 = 0
		self.k2 = 0
		self.error_1 = self.error_2 = 0
		self.error_1_pprev = self.error_2_pprev = 0
		self.error_1_prev = self.error_2_prev = 0

		# Variables de trabajo
		self.frame1 = None
		self.frame2 = None
		self.frame_filtered = None
		self.p1 = None
		self.p2 = None
		self.p3 = None
		self.p4 = None
		self.p5 = None
		self.a1 = None # Arco amigo
		self.a2 = None # Arco enemigo
		self.center = np.array([320, 240])
		self.objective = None

		# Parámetros de trabajo
		self.active = True       # Parámetro bajo el cual el Thread corre
		# Contador para ir cambiando los colores a utilizar
		# 0 -> parte trasera del auto; 1 -> parte delantera del auto; 2 -> pelota
		self.count = 0

		# Variable para manipular el número de prints
		self.key_pressed = False
		# Variable para enviar mensajes incluso si no hay visual
		self.wasd_mode = False
		self.wasd_time = 0
		self.kick_time = 0
		self.push = False
		self.AI_mode = False

		# Q-Table para AI
		# Condiciones:
		# 1 - Pelota está en lado amigo
		# 2 - Auto está atrás de la pelota
		# 3 - Enemigo está adelante de la pelota
		# 4 - Enemigo está en posició para pegar
		self.state = ()
		self.q_table = {
						():        "2",  # Cuidar pelota
						(1,2,3):   "3",  # Empujar pelota al arco
						(1,3,4):   "4",  # Defender como arquero
						(1,):       "4",  # Defender como arquero
						(1,2,3,4): "5",  # Defender como defensa
						(2,3):     "6",  # Meter gol pegando
						(2,):       "7",  # Meter gol empujando
						(1,2):     "7",  # Meter gol empujando
                        (1,2,4):     "7",  # Meter gol empujando
						}
		
	def parse_msg(self):
		try:
			motor1 = max(-p("MAX_VEL"), min(p("MAX_VEL"), int(self.motorRPM_1)))
			motor2 = max(-p("MAX_VEL"), min(p("MAX_VEL"), int(self.motorRPM_2)))
			self.antena.msg = p("MESSAGE").format(motor1= motor1, motor2= motor2)
		except ValueError:
			pass

	def thread_ver(self):
		# Windows
		cv2.namedWindow(p("MAIN_WINDOW")) #
		cv2.moveWindow(p("MAIN_WINDOW"), p("MW_X"), p("MW_Y")) #
		cv2.namedWindow(p("PROGRAM_WINDOW")) #
		cv2.moveWindow(p("PROGRAM_WINDOW"), p("PW_X"), p("PW_Y")) #
		self.antena.restart()
		
		while self.active:
			self.start = time.time()
			ret, self.frame1 = self.cap.read() #
			
			self.frame2 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2HSV)

			self.COLOR1 = self.filtro(self.c1)
			self.COLOR2 = self.filtro(self.c2)
			self.COLOR3 = self.filtro(self.c3)
			self.COLOR4 = self.filtro(self.c4)
			self.COLOR5 = self.filtro(self.c5)
			
			## --- Matemáticas --- ##
			self.mask()    # Calcular matrices de colores y combinarlas con la  original para tener la filtrada
			self.math()   # 

			## --- Mostrar en ventana --- ##
			self.mostrar(f"Angle: {round(np.degrees(self.angle), 1)} deg", 1)
			self.mostrar(f"Distance: {round(self.dist_mts, 2)} cm", 2)
			self.mostrar(f"Velocity: {round((self.motorRPM_1 + self.motorRPM_2)/2, 1)} RPM", 1, True)
			self.mostrar(f"Mensaje: {self.antena.msg}", 2, True)
			self.mostrar(f"Estado: {str(self.state)}", 3, True)
			
			## --- Mostrar pantallas y revisar evento de mouse --- ##
			cv2.imshow(p("PROGRAM_WINDOW"), self.frame_filtered)
			cv2.imshow(p("MAIN_WINDOW"), self.frame1)
			cv2.setMouseCallback(p("MAIN_WINDOW"), self.click_event)
			
			## --- Revisar inputs --- ##
			# Leer entrada del teclado
			self.keyboard()

			## --- Modo automático --- ##
			if self.AI_mode:
				# Actualiza la task según el estado del juego
				self.get_state()
				try:
					self.task = self.q_table[self.state]
				except KeyError:
					self.task = "4"  # En cualquier otro caso posible, defender el arco

			## --- Actualizar el mensaje de la antena --- ##
			self.task_manager()
			# Actualizar mensaje con PID
			self.pid_period = time.time() - self.start
			self.PID()
			# Modificar mensaje a enviar
			self.parse_msg()
		
		self.cap.release()
		cv2.destroyAllWindows()

	def filtro(self, col):
		if col is None:
			# Defoult: Rosado brillante y saturado
			return cv2.inRange(self.frame2, np.array(p("DEFAULT_COLOR")) - np.array([0,0,1]), np.array(p("DEFAULT_COLOR")))
		return cv2.inRange(self.frame2, col - self.rango, col + self.rango)

	def mostrar(self, txt, ID, *COL):
		col = 10
		if COL:
			col = 450
		cv2.putText(self.frame_filtered, str(txt), (col, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
		
	def alpha(self, v1, v2):
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
		else:
			return 0
		
	def limit(self, value):
		# Limita un valor a estar entre 0 y self.car_vel
		return max(min(value, p("MAX_VEL")), 0)
	
	def int_array(self, vector):
		return np.array([int(vector[0]), int(vector[1])])
		
	def math(self):
		if str(self.p1) != "None" and str(self.p2) != "None" and str(self.objective) != "None":
			# Función para determinar ángulo y distancia a objetivo
			cX1, cY1 = self.p1	# Retaguardia del auto
			cX2, cY2 = self.p2	# Vanguardia del auto
			cX3, cY3 = self.objective	# Objetivo
			

			# Vectores
			vector_C1_C2 = np.array([cX2-cX1, -(cY2-cY1)])
			vector_C1_C3 = np.array([cX3-cX1, -(cY3-cY1)])

			# Establecer ángulo = [-180°, 180°]
			self.angle = self.alpha(vector_C1_C2, vector_C1_C3)
			# Distancia en pixeles
			self.dist_pix = np.linalg.norm(vector_C1_C3)
			# Distancia en metros
			self.dist_mts = p("LARGO_AUTO")*np.linalg.norm(vector_C1_C3)/np.linalg.norm(vector_C1_C2)
			if str(self.dist_mts) == "nan" or str(self.dist_mts) == "inf":
				self.dist_mts = 0
		
		# Lo mismo, pero para el enemigo
		if str(self.p4) != "None" and str(self.p5) != "None" and str(self.p3) != "None":
			# Función para determinar ángulo y distancia a objetivo
			cX1, cY1 = self.p4	# Retaguardia del auto enemigo
			cX2, cY2 = self.p5	# Vanguardia del auto enemigo
			cX3, cY3 = self.p3	# Pelota

			# Vectores
			vector_C1_C2 = np.array([cX2-cX1, -(cY2-cY1)])
			vector_C1_C3 = np.array([cX3-cX1, -(cY3-cY1)])

			# Establecer ángulo = [-180°, 180°]
			self.angle_enemy = self.alpha(vector_C1_C2, vector_C1_C3)
			# Distancia en pixeles
			self.dist_pix_enemy = np.linalg.norm(vector_C1_C3)
			# Distancia en metros
			self.dist_mts_enemy = p("LARGO_AUTO")*np.linalg.norm(vector_C1_C3)/np.linalg.norm(vector_C1_C2)
			if str(self.dist_mts_enemy) == "nan" or str(self.dist_mts_enemy) == "inf":
				self.dist_mts_enemy = 0

	def mask(self):
		points = 0
		for p, c in zip(range(5), [self.COLOR1, self.COLOR2, self.COLOR3, self.COLOR4, self.COLOR5]):
			try:
				ret, thresh = cv2.threshold(c, 127, 255, 0)
				M = cv2.moments(thresh)
				X = int(M["m10"] / M["m00"])
				Y = int(M["m01"] / M["m00"])
				cv2.circle(self.frame1, (X, Y), 5, (255, 255, 255), -1)
			except ZeroDivisionError or NameError:
				if p <= 1:
					self.frame_filtered = self.frame1.copy()
				break
			else:
				if p == 0:
					self.p1 = np.array([X, Y])
					points += 1
				elif p == 1:
					self.p2 = np.array([X, Y])
					mask = cv2.bitwise_or(self.COLOR1, self.COLOR2)
					points += 1
				elif p == 2:
					self.p3 = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.COLOR3)
					points += 1
				elif p == 3:
					self.p4 = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.COLOR4)
					points += 1
				elif p == 4:
					self.p5 = np.array([X, Y])
					mask = cv2.bitwise_or(mask, self.COLOR5)
					points += 1
		
		if points >= 2:
			self.frame_filtered = cv2.bitwise_and(self.frame1, self.frame1, mask= mask)
			# --- DIBUJAR ---
			# Linea entre C1 y C2
			cv2.line(self.frame_filtered, self.p1, self.p2, (255, 255, 255), 3)
			if str(self.objective) != "None":
				# Linea entre C1 y C3
				cv2.line(self.frame_filtered, self.p1, self.objective, (255, 255, 255), 3)
			if points == 5:
				# Linea entre C4 y C5 (auto enemigo)
				cv2.line(self.frame_filtered, self.p4, self.p5, (125, 125, 125), 3)

		# Mostrar arcos
		arc = 0
		if str(self.a1) != "None":
			cv2.circle(self.frame1, self.a1, 5, (255, 100, 100), -1)
			cv2.circle(self.frame_filtered, self.a1, 5, (255, 100, 100), -1)
			arc += 1
		if str(self.a2) != "None":
			cv2.circle(self.frame1, self.a2, 5, (100, 100, 255), -1)
			cv2.circle(self.frame_filtered, self.a2, 5, (100, 100, 255), -1)
			arc += 1
		# Marcar centro
		if arc == 2:
			self.center = self.int_array(self.a1/2 + self.a2/2)
			cv2.circle(self.frame1, self.center, 3, (100, 255, 100), -1)
			cv2.circle(self.frame_filtered, self.center, 3, (100, 255, 100), -1)

	# --------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------

	def velocidad(self):
		try:
			# Entregar una velocidad dependiendo de la task
			if self.wasd_mode:
				if self.task == "0.1":
					return self.car_vel*self.sgn/2
				else:
					return self.car_vel/10

			elif self.task == "1" or self.task == "4" or self.task == "5" or self.task == "6":
				if self.dist_mts - p("LARGO_AUTO")/2 >= p("STOPPING_THRESHOLD"):
					return self.car_vel
				elif self.dist_mts - p("LARGO_AUTO")/2 <= p("STOP_THRESHOLD"):
					if self.task == "6" and self.dist_mts != 0:
						# Pequeño Glitch
						self.task = "6.1"
					return 0
				else:
					return (self.dist_mts - p("LARGO_AUTO")/2)*p("DIST_TO_PWR")
			
			elif self.task == "2":
				if self.dist_mts - p("LARGO_AUTO") >= p("STOPPING_THRESHOLD"):
					return self.car_vel
				elif self.dist_mts - p("LARGO_AUTO") >= p("STOP_BALL_THRESHOLD"):
					return (self.dist_mts - p("LARGO_AUTO"))*p("DIST_TO_PWR")
				else:
					return 0

			elif self.task == "3":
				return self.car_vel
			
			elif self.task == "6.1":
				print(self.objective)
				if abs(np.degrees(self.angle)) <= p("ANGLE_THRESHOLD"):
					self.task = "6.2"
					self.kick_time = 0
				return 0
			
			elif self.task == "6.2":
				if self.dist_mts - p("LARGO_AUTO")/2 >= p("STOPPING_THRESHOLD"):
					return (self.dist_mts - p("LARGO_AUTO")/2)*p("DIST_TO_PWR")
				elif self.dist_mts - p("LARGO_AUTO")/2 <= p("STOP_THRESHOLD"):
					self.task = "6.3"
					self.dist_push = np.linalg.norm(self.a2 - self.p1)
					return 0
				else:
					return (self.dist_mts - p("LARGO_AUTO")/2)

			elif self.task == "6.3":
				if not self.push:
					# Pegar un penal
					if self.kick_time == 0:
						self.kick_time = time.time()
					if time.time() - self.kick_time >= p("KICK_TIME"):
						self.kick_time = 0
						self.task = None
						return 0
					else:
						return p("MAX_VEL")
				else:
					# Para task 7
					if np.linalg.norm(self.a2 - self.p2) - p("LARGO_AUTO")/2 <= p("STOPPING_THRESHOLD"):
						self.push = False
						self.task = None
						return 0
					else:
						return (max(0, self.dist_push - np.linalg.norm(self.a2 - self.p2)) * p("DIST_TO_PWR"))**0.75
			
			else:
				return 0
				
		except TypeError:
			print(f"\033[1mWARNING:\033[0m Faltan elementos para completar la \033[1mTask {self.task}\033[0m")
			return 0
			
	def PID(self):
		## Definir constantes del PID
		self.k0 = p("kp")*(1 + p("ki")*self.pid_period + p("kd")/self.pid_period)
		self.k1 = -p("kp")*(1 + 2*p("kd")/self.pid_period)
		self.k2 = p("kp")*p("kd")/self.pid_period
				
		velocity = self.velocidad()
		if velocity != None:
			if np.degrees(abs(self.angle)) <= p("ANGLE_THRESHOLD"):
				self.error_1 = 0
				self.error_2 = 0
			else:
				if self.angle >= 0:
					self.error_1 = min(self.angle, np.tan(self.angle/2))
					self.error_2 = max(-self.angle, np.tan(-self.angle/2))
				else:
					self.error_1 = max(self.angle, np.tan(self.angle/2))
					self.error_2 = min(-self.angle, np.tan(-self.angle/2))
			# Actualizar las velocidades de las ruedas
			self.motorRPM_1 = velocity + self.k0*self.error_1 + self.k1*self.error_1_prev + self.k2*self.error_1_pprev
			self.motorRPM_2 = velocity + self.k0*self.error_2 + self.k1*self.error_2_prev + self.k2*self.error_2_pprev

			# Actualizar variables previas
			self.error_1_pprev = self.error_1_prev
			self.error_2_pprev = self.error_2_prev
			self.error_1_prev = self.error_1
			self.error_2_prev = self.error_2
			
	def click_event(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			next_color = self.frame2[y][x]
			if not self.enemy:
				if self.count in [3, 4]:
					self.count = 5
			if self.count == 0:
				self.c1 = next_color
			if self.count == 1:
				self.c2 = next_color
			if self.count == 2:
				self.c3 = next_color
			if self.count == 3:
				self.c4 = next_color
			if self.count == 4:
				self.c5 = next_color
			if self.count == 5:
				self.a1 = np.array([x, y])
			if self.count == 6:
				self.a2 = np.array([x, y])

			self.count += 1
			if self.count == 7:
				self.count = 5
		
		if event == cv2.EVENT_RBUTTONDOWN:
			self.c1 = None
			self.c2 = None
			self.c3 = None
			self.c4 = None
			self.c5 = None
			self.a1 = None
			self.a2 = None
			self.center = np.array([320, 240])
			self.count = 0
	
	def keyboard(self):
		# Leer comandos del teclado
		key = cv2.waitKey(5)
		# Revisar si ha finalizado el programa
		if key == 27: #
			self.antena.active = False
			self.active = False
		else:
			try:
				code = p("keys")[str(key)]
			except KeyError:
				if key != -1:
					print(key)
			else:
				self.key_pressed = True
				self.wasd_mode = False
				if self.sgn == -1 and self.task == "0.1":
					self.c1, self.c2 = self.c2, self.c1
				self.sgn = 1

				if code.isnumeric():
					self.task = code
				elif code == "reset": # Delete
					self.reset()
				elif code == "stop":  # Space
					self.task = None
				elif code == "up_vel": # W
					self.car_vel += 10
				elif code == "dw_vel": # S
					self.car_vel -= 10
				elif code == "max_vel": # +
					self.car_vel = p("MAX_VEL")
				elif code == "rst_vel": # -
					self.car_vel = p("CAR_VEL")
				elif code == "w": # w
					self.wasd_mode = True
					self.task = "0.1"
				elif code == "a": # a
					self.wasd_mode = True
					self.task = "0.2"
				elif code == "s": # s
					self.wasd_mode = True
					self.task = "0.1"
					if self.sgn != -1:
						self.c1, self.c2 = self.c2, self.c1
					self.sgn = -1
				elif code == "d": # d
					self.wasd_mode = True
					self.task = "0.2"
					self.sgn = -1
				elif code == "enemy":  # e
					if self.enemy:
						self.enemy = False
						self.p4 = None
						self.p5 = None
						self.c4 = None
						self.c5 = None
					else:
						self.enemy = True
						self.count = 3
				elif code == "help":  # h
					self.instructions()
				elif code == "coms":
					if self.antena.active:
						self.antena.active = False
					else:
						self.antena.restart()
				elif code == "AI":
					self.AI_mode = not self.AI_mode
				else:
					self.AI_mode = False
	
	def task_manager(self):
		try:
			if self.task == "0.1": 
				self.objective = 2*self.p2 - self.p1
			
			elif self.task == "0.2":
				extra = self.sgn*(self.p2 - self.p1)
				extra = np.array([extra[1], -extra[0]])
				self.objective = self.int_array(self.p1*8/10 + self.p2*2/10 + extra)

			elif self.task == "1": self.objective = self.center # Go to the center

			elif self.task == "2": self.objective = self.p3 # Frenar frente a la pelota
			
			elif self.task == "3": self.objective = self.p3 # Buscar pelota y empujarla sin parar

			elif self.task == "4": self.objective = self.a1 # Distancia del robot al arco
			
			elif self.task == "5": self.objective = self.a1//2 + self.p3//2 # Defender entre el arco y la pelota
			
			elif self.task == "6":
				# Primero vamos a la pelota nos detenemos frente a ella (objective=pelota)
				ball_arc_dist = p("LARGO_AUTO")*np.linalg.norm(self.a2 - self.p3)/np.linalg.norm(self.p2 - self.p1)
				k = -p("PENALTY_SPACE_1")/ball_arc_dist
				
				self.objective = self.int_array(self.p3 + (self.a2 - self.p3)*k)

			elif self.task == "6.1": self.objective = self.p3 # Acercarse al auto para penal
			
			elif self.task == "6.2": 
				ball_arc_dist = p("LARGO_AUTO")*np.linalg.norm(self.a2 - self.p3)/np.linalg.norm(self.p2 - self.p1)
				k = -p("PENALTY_SPACE_2")/ball_arc_dist
				
				self.objective = self.int_array(self.p3 + (self.a2 - self.p3)*k)
				
			elif self.task == "6.3":
				if not self.push:
					self.objective = self.p3
				else:
					p21 = self.p2 - self.p1
					d = self.p3 - self.p1
					self.objective = self.int_array( (p21*(p21.dot(d)/np.linalg.norm(p21)**2) + self.p1)/2 + self.p3/2 )

			elif self.task == "7":
				self.task = "6"
				self.push = True
			
			else:
				self.angle = 0
				self.dist_pix = 0
				self.dist_mts = 0
				self.objective = None
			
		except TypeError:
			if self.key_pressed:
				print(f"\033[1mWARNING:\033[0m Faltan elementos para completar la \033[1mTask {self.task}\033[0m")
				self.key_pressed = False
	
	def instructions(self):
		print("\n\033[1m ----- Instrucciones -----\033[0m")
		print(f"\033[1m> Esc:\033[0m Finaliza el programa")
		print(f"\033[1m> e:\033[0m Toggle show/hide enemy")
		print(f"\033[1m> Space:\033[0m Stop car")
		print(f"\033[1m> 1:\033[0m Inicia la Task 1 - Moverse al centro")
		print(f"\033[1m> 2:\033[0m Inicia la Task 2 - Moverse hasta la pelota sin tocarla")
		print(f"\033[1m> 3:\033[0m Inicia la Task 3 - Empujar la pelota en línea recta")
		print(f"\033[1m> 4:\033[0m Inicia la Task 4 - Defender el arco como arquero")
		print(f"\033[1m> 5:\033[0m Inicia la Task 5 - Defender el arco como defensa")
		print(f"\033[1m> 6:\033[0m Inicia la Task 6 - Penalty")
		print(f"\033[1m> 7:\033[0m Inicia la Task 7 - Meter gol")
		print(f"\033[1m> p:\033[0m Inicia el modo automático")
		print(f"\033[1m> o:\033[0m Reinicia las comunciaciones")
		print(f"\033[1m> wasd:\033[0m Control manual")
		print(f"\033[1m> WS:\033[0m Aumentar/Disminuir la velocidad")
		print(f"\033[1m> +:\033[0m Setea la velocidad en la máxima")
		print(f"\033[1m> -:\033[0m Reinicia la velocidad a su valor predeterminado")

	def reset(self):
		self.task = None

		self.c1 = None
		self.c2 = None
		self.c3 = None
		self.c4 = None
		self.c5 = None
		self.enemy = False

		# Valores para controlador
		self.angle = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.angle_enemy = 0
		self.dist_pix_enemy = 0
		self.dist_mts_enemy = 0
		self.motorRPM_1 = 0
		self.motorRPM_2 = 0
		self.car_vel = p("CAR_VEL")

		# Variables de trabajo
		self.frame_filtered = None
		self.p1 = None
		self.p2 = None
		self.p3 = None
		self.p4 = None
		self.p5 = None
		self.a1 = None # Arco amigo
		self.a2 = None # Arco enemigo
		self.center = np.array([320, 240])
		self.objective = None

		self.start = 0
		self.pid_period = 0
		self.error_1 = self.error_2 = 0
		self.error_1_pprev = self.error_2_pprev = 0
		self.error_1_prev = self.error_2_prev = 0

		# Parámetros de trabajo
		self.active = True       # Parámetro bajo el cual el Thread corre
		# Contador para ir cambiando los colores a utilizar
		self.count = 0

		# Variable para manipular el número de prints
		self.key_pressed = False
		# Variable para enviar mensajes incluso si no hay visual
		self.wasd_mode = False
		self.wasd_time = 0
		self.kick_time = 0
		self.push = False
		self.AI_mode = False

		# AI
		self.state = ()

	## --- Artifitial Intelligence --- ##
	def get_state(self):
		# Condiciones:
		# 1 - Pelota está en lado amigo
		# 2 - Auto está atrás de la pelota
		# 3 - Enemigo está adelante de la pelota
		# 4 - Enemigo está en posició para pegar
		self.state = []
		# Orientar
		side = True
		try:
			if self.a1[0] > self.a2[0]:
				side = False
		except TypeError:
			pass
		
		try:
			if side:
				if self.p3[0] <= self.center[0]:
					self.state.append(1)
			else:
				if self.p3[0] >= self.center[0]:
					self.state.append(1)
		except TypeError:
			pass
		
		try:
			if side:
				if self.p2[0] <= self.p3[0]:
					self.state.append(2)
			else:
				if self.p2[0] >= self.p3[0]:
					self.state.append(2)
		except TypeError:
			pass

		try:
			if side:
				if self.p5[0] >= self.p3[0]:
					self.state.append(3)
			else:
				if self.p5[0] <= self.p3[0]:
					self.state.append(3)
		except TypeError:
			pass

		try:
			if self.dist_mts_enemy <= 40 and abs(self.angle_enemy) <= 1:
				self.state.append(4)
		except TypeError:
			pass
		
		self.state = tuple(self.state)

# Leer parámetros
def p(arg):
    with open("parametros v2.json", "r") as parametros:
        data = json.load(parametros)
        valor = data[arg]
    return valor

if __name__ == '__main__':
	antena = Coms()
	camera = Vision(nCam= 1, antena= antena)
	camera.thread.start()