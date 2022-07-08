import numpy as np
import cv2
import json
import time
import serial
from threading import Thread


class Coms:

	def __init__(self):
		self.msg = p("MESSAGE").format(motor1= 0, motor2= 0)
		self.active = True
		# seria.Serial nos permite abrir el puerto COM deseado
		self.ser = serial.Serial(p("COM"), baudrate = p("BR"), timeout = 1)
		self.thread = Thread(target= self.thread_comunicar, daemon= False)

	def thread_comunicar(self):
		while self.active:
			# El Ambos mensajes que estan en formato Sring deben ser transformados en un arreglo de bytes mediante la funcion .encode
			msgencode = str.encode(self.msg) 
			# .write nos permite enviar el arreglo de bytes correspondientes a los mensajes
			self.ser.write(msgencode);
			time.sleep(p("PERIOD_COMS"))
		
		# Stop the car
		msgencode = str.encode(p("MESSAGE").format(motor1= 0, motor2= 0))
		self.ser.write(msgencode);
		self.ser.close()
		
class Vision:

	def __init__(self, nCam= 0, antena= None):
		self.antena = antena
		
		# Rango de error y colores predeterminados
		self.rango = np.array(p("RANGE"))
		self.c1 = None
		self.c2 = None
		self.c3 = None
		
		# Inicializar cámara
		self.cap = cv2.VideoCapture(nCam) #
		self.thread = Thread(target= self.thread_ver, daemon= False)

		# Valores para controlador
		self.angle = 0
		self.dist_pix = 0
		self.dist_mts = 0
		self.motorRPM_1 = 0
		self.motorRPM_2 = 0
		self.motorRPM_1_PREV = 0
		self.k0 = p("KP")*(1 + p("KI")*p("PERIOD_VISION") + p("KD")/p("PERIOD_VISION"))
		self.k1 = -p("KP")*(1 + 2*p("KD")/p("PERIOD_VISION"))
		self.k2 = p("KP")*p("KD")/p("PERIOD_VISION")
		self.error1 = 0
		self.error1_PREV = 0
		self.error1_PPREV = 0

		# Variables de trabajo
		self.frame1 = None
		self.frame2 = None
		self.frame_filtered = None
		self.p1 = None
		self.p2 = None
		self.p3 = None

		# Parámetros de trabajo
		self.angle_fixed = False
		self.active = True       # Parámetro bajo el cual el Thread corre
		self.no_visual = False   # Cuando no se encuentra el auto, se le dice que se detenga
		# Contador para ir cambiando los colores a utilizar
		# 0 -> parte trasera del auto; 1 -> parte delantera del auto; 2 -> pelota
		self.count = 0
		self.start = 0
		
	def parse_msg(self):
		if self.no_visual:
			self.antena.msg = p("MESSAGE").format(motor1= 0, motor2= 0)
		else:
			self.antena.msg = p("MESSAGE").format(motor1= int(self.motorRPM_1), motor2= int(self.motorRPM_2))

	def PID(self):
		self.PID_angle()
	
		if self.angle_fixed:
			self.PID_vel()
			

	def PID_angle(self):
		power = p("MAX_TURN")*np.deg2rad(self.angle)
		if self.angle > p("epsilon"):
			self.motorRPM_1 = power
			self.motorRPM_2 = 0
			self.angle_fixed = False
		elif self.angle < -p("epsilon"):
			self.motorRPM_2 = -power
			self.motorRPM_1 = 0
			self.angle_fixed = False
		else:
			self.angle_fixed = True
		
		
	def PID_vel(self):
		# self.error1 = (self.dist_pix - p("DIST_REF"))
		# self.motorRPM_1 = self.motorRPM_1_PREV + self.k0*self.error1 + self.k1*self.error1_PREV + self.k2*self.error1_PPREV
		# self.motorRPM_2 = self.motorRPM_1
		# self.motorRPM_1_PREV = self.motorRPM_1
		# self.error1_PPREV = self.error1_PREV
		# self.error1_PREV = self.error1
		self.motorRPM_1 = self.dist_pix - p("PIX_REF")
		self.motorRPM_2 = self.dist_pix - p("PIX_REF")
			

	def thread_ver(self):
		# Windows
		cv2.namedWindow(p("MAIN_WINDOW")) #
		cv2.moveWindow(p("MAIN_WINDOW"), p("MW_X"), p("MW_Y")) #
		cv2.namedWindow(p("PROGRAM_WINDOW")) #
		cv2.moveWindow(p("PROGRAM_WINDOW"), p("PW_X"), p("PW_Y")) #
		while self.active:
			self.start = time.time()
			ret, self.frame1 = self.cap.read() #
			
			self.frame2 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2HSV)

			self.COLOR1 = self.filtro(self.c1)
			self.COLOR2 = self.filtro(self.c2)
			self.COLOR3 = self.filtro(self.c3)
			
			## --- Matemáticas --- ##
			self.mask()    # Calcular matrices de colores y combinarlas con la  original para tener la filtrada
			self.math()   # 
			self.mostrar(f"Angle: {round(self.angle, 1)} deg", 1)
			self.mostrar(f"Distance: {int(self.dist_pix)} pix", 2)
			self.mostrar(f"Distance: {round(self.dist_mts, 2)} cm", 3)
			
			# Mostrar pantallas y revisar evento de mouse
			cv2.imshow(p("PROGRAM_WINDOW"), self.frame_filtered)
			cv2.imshow(p("MAIN_WINDOW"), self.frame1)
			cv2.setMouseCallback(p("MAIN_WINDOW"), self.click_event)
			
			# Revisar si ha finalizado el programa
			if cv2.waitKey(1) & 0xFF == 27: #
				self.active = False

			# Actualizar el mensaje de la antena
			self.PID()
			self.parse_msg()

			# Periodo de trabajo
			time.sleep(max(p("PERIOD_VISION") - (time.time() - self.start), 0))
		
		self.cap.release()
		cv2.destroyAllWindows()
		self.antena.active = False
		self.antena.thread.join()

	def click_event(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			next_color = self.frame2[y][x]
			if self.count == 0:
				self.c1 = next_color
			if self.count == 1:
				self.c2 = next_color
			if self.count == 2:
				self.c3 = next_color

			self.count += 1
			if self.count == 3:
				self.count = 0
		if event == cv2.EVENT_RBUTTONDOWN:
			self.c1 = None
			self.c2 = None
			self.c3 = None
			self.count = 0
	
	def filtro(self, col):
		if col is None:
			return cv2.inRange(self.frame2, np.array([0,0,0]), np.array([0,0,0]))
		return cv2.inRange(self.frame2, col - self.rango, col + self.rango)

	def mostrar(self, txt, ID):
		cv2.putText(self.frame_filtered, str(txt), (10, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

	def alpha(self, sin, cos):
		if sin >= 0 and cos >= 0:
			return np.arcsin(sin)
		elif sin >= 0 and cos < 0:
			return np.pi - np.arccos(-cos)
		elif sin < 0 and cos < 0:
			return np.arccos(-cos) - np.pi
		elif sin < 0 and cos >= 0:
			return np.arcsin(sin)
		return 0
		
	def math(self):
		if (self.p1 is None) or (self.p2 is None) or (self.p3 is None):
			pass
		else:
			# Función para determinar ángulo y distancia a objetivo
			cX1, cY1 = self.p1	# Retaguardia del auto
			cX2, cY2 = self.p2	# Vanguardia del auto
			cX3, cY3 = self.p3	# Objetivo
			
			# Vectores
			vector_C1_C2 = np.array([cX2-cX1, -(cY2-cY1)])
			vector_C1_C3 = np.array([cX3-cX1, -(cY3-cY1)])

			# Producto punto y cruz
			sin_alpha = np.cross(vector_C1_C2, vector_C1_C3) / (np.linalg.norm(vector_C1_C2)*np.linalg.norm(vector_C1_C3))
			cos_alpha = vector_C1_C2.dot(vector_C1_C3) / (np.linalg.norm(vector_C1_C2)*np.linalg.norm(vector_C1_C3))

			# Usar sin y cos para determinar ángulo = [-180°, 180°]
			self.angle = np.degrees(self.alpha(sin_alpha, cos_alpha))
			# Distancia en pixeles
			self.dist_pix = np.linalg.norm(vector_C1_C3)
			# Distancia en metros
			self.dist_mts = p("LARGO_AUTO")*np.linalg.norm(vector_C1_C3)/np.linalg.norm(vector_C1_C2)
			if str(self.dist_mts) == "nan" or str(self.dist_mts) == "inf":
				self.dist_mts = 0

	def mask(self):
		try:
			for p, c in zip(range(3), [self.COLOR1, self.COLOR2, self.COLOR3]):
				ret, thresh = cv2.threshold(c, 127, 255, 0)
				M = cv2.moments(thresh)
				X = int(M["m10"] / M["m00"])
				Y = int(M["m01"] / M["m00"])
				cv2.circle(self.frame1, (X, Y), 5, (255, 255, 255), -1)
				if p == 0:
					self.p1 = np.array([X, Y])
				elif p == 1:
					self.p2 = np.array([X, Y])
				elif p == 2:
					self.p3 = np.array([X, Y])
			
			mask = cv2.bitwise_or(cv2.bitwise_or(self.COLOR1, self.COLOR2), self.COLOR3)
			self.frame_filtered = cv2.bitwise_and(self.frame1, self.frame1, mask= mask)

			# --- DIBUJAR ---
			# Linea entre C1 y C2
			cv2.line(self.frame_filtered, self.p1, self.p2, (255, 255, 255), 3)
			# Linea entre C1 y C3
			cv2.line(self.frame_filtered, self.p1, self.p3, (255, 255, 255), 3)

		except ZeroDivisionError or NameError:
			# En caso de error al calcular los centros de masa, devolver la pantalla principal y detener el auto
			self.frame_filtered = self.frame1.copy()
			self.no_visual = True
		else:
			self.no_visual = False


# Leer parámetros
def p(arg):
    with open("parametros.json", "r") as parametros:
        data = json.load(parametros)
        valor = data[arg]
    return valor

if __name__ == '__main__':
	antena = Coms()
	camera = Vision(nCam= 0, antena= antena)
	camera.thread.start()
	antena.thread.start()