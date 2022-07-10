from matplotlib.ft2font import HORIZONTAL
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
			try:
				# El Ambos mensajes que estan en formato Sring deben ser transformados en un arreglo de bytes mediante la funcion .encode
				msgencode = str.encode(self.msg)
				# .write nos permite enviar el arreglo de bytes correspondientes a los mensajes
				self.ser.write(msgencode)
			except:
				self.breaked = True
				self.active = False
				break
			else:
				time.sleep(p("PERIOD_COMS"))
		
		# Stop the car
		if not self.breaked:
			msgencode = str.encode(p("MESSAGE").format(motor1= 0, motor2= 0))
			self.ser.write(msgencode);
			self.ser.close()
		print("Comunicación por BlueTooth terminada")

	def restart(self):
		if self.active:
			self.active = False
			self.thread.join()
		else:
			try:
				# Probar comunicación
				self.ser = serial.Serial(p("COM"), baudrate = p("BR"), timeout = 1)
			except:
				# En caso de error, finalizar comunicación
				print("\033[1mWARNING:\033[0m Fallo de comunicación por BlueTooth")
			else:
				print("Conexión por BlueTooth establecida")
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
		# self.cap.set(cv2.CAP_PROP_SETTINGS, 1)
		self.thread = Thread(target= self.thread_ver, daemon= False)

		# Valores para controlador
		self.angle = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.motorRPM_1 = 0
		self.motorRPM_2 = 0
		self.car_vel = p("CAR_VEL")
		self.turn_vel = p("TURN_VEL")

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
		self.angle_fixed = False
		self.active = True       # Parámetro bajo el cual el Thread corre
		self.no_visual = False   # Cuando no se encuentra el auto, se le dice que se detenga
		# Contador para ir cambiando los colores a utilizar
		# 0 -> parte trasera del auto; 1 -> parte delantera del auto; 2 -> pelota
		self.count = 0
		self.start = 0

		# Variable para manipular el número de prints
		self.key_pressed = False
		# Variable para enviar mensajes incluso si no hay visual
		self.wasd_mode = False
		self.wasd_time = 0
		self.kick_time = 0
		self.push = False
		
	def parse_msg(self):
		if self.no_visual and self.task != "0":
			self.set_speed(0)
		self.antena.msg = p("MESSAGE").format(motor1= int(self.motorRPM_1), motor2= int(self.motorRPM_2))

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
			self.mostrar(f"Angle: {round(np.degrees(self.angle), 1)} deg", 1)
			self.mostrar(f"Distance: {int(self.dist_pix)} pix", 2)
			self.mostrar(f"Distance: {round(self.dist_mts, 2)} cm", 3)
			self.mostrar(f"Velocity: {round((self.motorRPM_1 + self.motorRPM_2)/2, 2)} RPM", 4)
			self.mostrar(f"Mensaje: {self.antena.msg}", 1, True)
			
			# Mostrar pantallas y revisar evento de mouse
			cv2.imshow(p("PROGRAM_WINDOW"), self.frame_filtered)
			cv2.imshow(p("MAIN_WINDOW"), self.frame1)
			cv2.setMouseCallback(p("MAIN_WINDOW"), self.click_event)
			
			# Revisar inputs
			self.keyboard()

			# Actualizar el mensaje de la antena
			self.task_manager()
			self.parse_msg()

			# Periodo de trabajo
			time.sleep(max(p("PERIOD_VISION") - (time.time() - self.start), 0))
		
		self.cap.release()
		cv2.destroyAllWindows()

	def filtro(self, col):
		if col is None:
			# Defoult: Rosado brillante y saturado
			return cv2.inRange(self.frame2, np.array(p("DEFAULT_COLOR")) - np.array([0,0,1]), np.array(p("DEFAULT_COLOR")))
		return cv2.inRange(self.frame2, col - self.rango, col + self.rango)

	def mostrar(self, txt, ID, *arg):
		if arg:
			cv2.putText(self.frame_filtered, str(txt), (450, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (155, 155, 155), 1)
		else:
			cv2.putText(self.frame_filtered, str(txt), (10, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
		

	def alpha(self, v1, v2):
		# Producto punto y cruz
		sin = np.cross(v1, v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
		cos = v1.dot(v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))
		if sin >= 0 and cos >= 0:
			self.angle = np.arcsin(sin)
		elif sin >= 0 and cos < 0:
			self.angle = np.pi - np.arccos(-cos)
		elif sin < 0 and cos < 0:
			self.angle = np.arccos(-cos) - np.pi
		elif sin < 0 and cos >= 0:
			self.angle = np.arcsin(sin)
		else:
			self.angle = 0
		
	def limit(self, value):
		# Limita un valor a estar entre 0 y self.car_vel
		return max(min(value, p("MAX_VEL")), 0)
		
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
			self.alpha(vector_C1_C2, vector_C1_C3)
			# Distancia en pixeles
			self.dist_pix = np.linalg.norm(vector_C1_C3)
			# Distancia en metros
			self.dist_mts = p("LARGO_AUTO")*np.linalg.norm(vector_C1_C3)/np.linalg.norm(vector_C1_C2)
			if str(self.dist_mts) == "nan" or str(self.dist_mts) == "inf":
				self.dist_mts = 0

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
					self.no_visual = True
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
					if str(self.objective) == "None":
						self.objective = self.p3
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
			self.no_visual = False
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
		if str(self.a1) != "None":
			cv2.circle(self.frame1, self.a1, 5, (255, 100, 100), -1)
			cv2.circle(self.frame_filtered, self.a1, 5, (255, 100, 100), -1)
		if str(self.a2) != "None":
			cv2.circle(self.frame1, self.a2, 5, (100, 100, 255), -1)
			cv2.circle(self.frame_filtered, self.a2, 5, (100, 100, 255), -1)

	# --------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------
	def erf(self):
		s = self.dist_mts - p("LARGO_AUTO")/2
		return self.limit(p("EXTRA_POWER")*s)
	
	def PID(self):
		# This PID gets to and stop at the objective
		turn_power = p("EXTRA_TURN")*self.turn_vel*self.angle
		if self.push:
			turn_power *= 0.005
		# Rotate the car until threshold
		if np.degrees(self.angle) > p("ANGLE_THRESHOLD_MAX")/2:
			self.motorRPM_1 = turn_power*1.5
			self.motorRPM_2 = -turn_power*0.5
		elif np.degrees(self.angle) < -p("ANGLE_THRESHOLD_MAX")/2:
			self.motorRPM_2 = -turn_power*1.5
			self.motorRPM_1 = turn_power*0.5
		else:
			# Set velocity according to distance using erf() function
			speed = self.erf()
			if self.push:
				speed *= 0.8
			if np.degrees(self.angle) >= p("ANGLE_THRESHOLD_MIN")/2:
				self.motorRPM_1 = speed + self.angle*p("VEL_PWR")
				self.motorRPM_2 = speed - self.angle*p("VEL_PWR")
			elif np.degrees(self.angle) <= -p("ANGLE_THRESHOLD_MIN")/2:
				self.motorRPM_1 = speed - self.angle*p("VEL_PWR")
				self.motorRPM_2 = speed + self.angle*p("VEL_PWR")
			else:
				self.set_speed(speed)

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
			self.count = 0
	
	def keyboard(self):
		# Leer comandos del teclado
		key = cv2.waitKey(5)
		# Revisar si ha finalizado el programa
		if key == 27: #
			self.antena.active = False
			try:
				self.antena.thread.join()
			except RuntimeError:
				pass
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
				if code.isnumeric():
					self.task = code
				elif code == "reset": # Delete
					self.reset()
				elif code == "stop":  # Space
					self.set_speed(0)
					self.task = None
				elif code == "up_vel": # W
					self.car_vel += 10
					self.set_speed(self.car_vel)
				elif code == "dw_vel": # S
					self.car_vel -= 10
					self.set_speed(self.car_vel)
				elif code == "up_turn": # D
					self.turn_vel += 10
				elif code == "dw_turn": # A
					self.turn_vel -= 10
				elif code == "w": # w
					self.set_speed(self.car_vel)
					self.task = "0"
				elif code == "a": # a
					self.motorRPM_1 = self.turn_vel*1.5
					self.motorRPM_2 = -self.turn_vel*0.5
					self.task = "0"
				elif code == "s": # s
					self.set_speed(-self.car_vel)
					self.task = "0"
				elif code == "d": # d
					self.motorRPM_1 = -self.turn_vel*0.5
					self.motorRPM_2 = self.turn_vel*1.5
					self.task = "0"
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
	
	def task_manager(self):
		try:
			if self.task == "0":
				# Mandar el comando WASD por T segundos
				if not self.wasd_mode:
					self.wasd_mode = True
					self.wasd_time = time.time()
				elif time.time() - self.wasd_time >= p("WASD_TIME"):
					self.task = None
					self.wasd_mode = False
					self.set_speed(0)

			elif self.task == "1":
				# Go to the center
				self.objective = self.center
				if self.dist_mts - p("LARGO_AUTO")/2 <= p("CENTER_THRESHOLD"):
					self.set_speed(0)
				else:
					self.PID()

			elif self.task == "2":
				# Frenar frente a la pelota
				self.objective = self.p3
				if self.dist_mts - p("LARGO_AUTO") <= p("BALL_THRESHOLD"):
					self.set_speed(0)
				else:
					self.PID()
			
			elif self.task == "3":
				# Buscar pelota y empujarla sin parar
				self.objective = self.p3
				if self.dist_mts - p("LARGO_AUTO") <= p("BALL_THRESHOLD"):
					self.task = "3.1"
				else:
					self.PID()
			
			elif self.task == "3.1":
				self.set_speed(self.car_vel*0.5)

			elif self.task == "4":
				# Distancia del robot al arco
				self.objective = self.a1
				if self.dist_mts - p("LARGO_AUTO") <= p("ARC_THRESHOLD"):
					self.set_speed(0)
				else:
					self.PID()
			
			elif self.task == "5":
				# Defender entre el arco y la pelota
				self.objective = self.a1//2 + self.p3//2
				if self.dist_mts - p("LARGO_AUTO")/2 <= p("ARC_THRESHOLD"):
					self.set_speed(0)
				else:
					self.PID()
			
			elif self.task == "6":
				# Primero vamos a la pelota nos detenemos frente a ella (objective=pelota)
				# Luego le pegamos hasta que llegue al arco (objective=a2)
				ball_arc_dist = p("LARGO_AUTO")*np.linalg.norm(self.a2 - self.p3)/np.linalg.norm(self.p2 - self.p1)
				k = -p("PENALTY_SPACE")/ball_arc_dist
				self.objective = self.p3 + (self.a2 - self.p3)*k
				self.objective = np.array([int(self.objective[0]), int(self.objective[1])])
				# Trabajar con valores enteros
				if self.dist_mts - p("LARGO_AUTO")/2 <= p("ARC_THRESHOLD"):
					self.task = "6.1"
					self.objective = self.a2
				else:
					self.PID()
			
			elif self.task == "6.1":
				# Se pone a una distancia de 10 cm de la pelota, se detiene y la golpea
				turn_power = self.turn_vel*self.angle
				if np.degrees(self.angle) > p("ANGLE_THRESHOLD_MIN"):
					self.motorRPM_1 = turn_power*0.5
					self.motorRPM_2 = -turn_power*0.8
				elif np.degrees(self.angle) < -p("ANGLE_THRESHOLD_MIN"):
					self.motorRPM_2 = -turn_power*0.5
					self.motorRPM_1 = turn_power*0.8
				else:
					self.task = "6.2"
					self.kick_time = 0
			
			elif self.task == "6.2":
				if not self.push:
					if self.kick_time == 0:
						self.kick_time = time.time()
					if time.time() - self.kick_time >= p("KICK_TIME"):
						self.set_speed(0)
						self.kick_time = 0
						self.task = 0
					else:
						self.set_speed(p("MAX_VEL"))
				else:
					if self.dist_mts - p("LARGO_AUTO")/2 <= p("ARC_THRESHOLD"):
						self.set_speed(0)
						self.push = False
						self.task = 0
					else:
						self.objective = self.p3
						self.PID()

			elif self.task == "7":
				self.task = "6"
				self.push = True
			
			elif self.task == "8":
				self.objective = self.p4//2 + self.p5//2
				self.PID()

			else:
				self.objective = self.p3
			
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
	
	def set_speed(self, speed):
		self.motorRPM_1 = self.motorRPM_2 = speed

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
		self.motorRPM_1 = 0
		self.motorRPM_2 = 0
		self.car_vel = p("CAR_VEL")
		self.turn_vel = p("TURN_VEL")

		# Variables de trabajo
		self.frame_filtered = None
		self.p1 = None
		self.p2 = None
		self.p3 = None
		self.p4 = None
		self.p5 = None
		self.a1 = None # Arco amigo
		self.a2 = None # Arco enemigo
		self.objective = None

		# Parámetros de trabajo
		self.angle_fixed = False
		self.active = True       # Parámetro bajo el cual el Thread corre
		self.no_visual = False   # Cuando no se encuentra el auto, se le dice que se detenga
		# Contador para ir cambiando los colores a utilizar
		# 0 -> parte trasera del auto; 1 -> parte delantera del auto; 2 -> pelota
		self.count = 0
		self.start = 0

		# Variable para manipular el número de prints
		self.key_pressed = False
		# Variable para enviar mensajes incluso si no hay visual
		self.wasd_mode = False
		self.wasd_time = 0
		self.kick_time = 0
		self.push = False

# Leer parámetros
def p(arg):
    with open("parametros v1.json", "r") as parametros:
        data = json.load(parametros)
        valor = data[arg]
    return valor

if __name__ == '__main__':
	antena = Coms()
	camera = Vision(nCam= 1, antena= antena)
	camera.thread.start()