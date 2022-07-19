import json
import time
import serial
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal

P_ROUTE = "parameters/coms_parameters.json"

class BTComs(QObject):

	def __init__(self):
		super().__init__()
		self.msg = self.p("MESSAGE").format(motor1= 0, motor2= 0)
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
				time.sleep(self.p("PERIOD_COMS"))
		
		if not self.breaked:
			# Stop the car
			msgencode = str.encode(self.p("MESSAGE").format(motor1= 0, motor2= 0))
			self.ser.write(msgencode)
			self.ser.close()
		else:
			self.breaked = False
		print("\033[1mMESSAGE:\033[0m BlueTooth communication terminated")

	def set_message(self, msg_tuple):
		self.msg = self.p("MESSAGE").format(motor1= round(msg_tuple[0], 4), motor2= round(msg_tuple[1], 4))


	def restart(self):
		self.end()

		try:
			# Probar comunicación
			self.ser = serial.Serial(self.p("COM"), baudrate = self.p("BR"), timeout = 1)
		except serial.serialutil.SerialException:
			# En caso de error, finalizar comunicación
			print("\033[1mWARNING:\033[0m BlueTooth communication failure")
		else:
			print("\033[1mMESSAGE:\033[0m BlueTooth communication succesfully established")
			self.active = True
			self.thread = Thread(target= self.thread_comunicar, daemon= False)
			self.thread.start()
	
	def end(self):
		self.active = False
		self.breaked = False
		self.ser = None
		self.thread = None

	def p(self, parameter):
		with open(P_ROUTE, "r") as file:
			data = json.load(file)
			try:
				return data[parameter]
			except KeyError:
				print(f"\033[1mWARNING: [BTComs]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
				return None


class SimComs(QObject):

	send_message_signal = pyqtSignal(tuple)

	def __init__(self):
		super().__init__()
		self.msg = (0,0)
		self.active = False
		self.thread = None
		
	def thread_comunicar(self):
		while self.active:
			
			self.send_message_signal.emit(self.msg)
			time.sleep(self.p("PERIOD_COMS"))

		self.send_message_signal.emit((0,0))
		
		print("\033[1mMESSAGE:\033[0m Communication terminated")

	def set_message(self, msg_tuple):
		self.msg = (round(msg_tuple[0], 4), round(msg_tuple[1], 4))

	def restart(self):
		self.end()
		
		print("\033[1mMESSAGE:\033[0m Communication established succesfully")
		self.active = True
		self.thread = Thread(target= self.thread_comunicar, daemon= False)
		self.thread.start()
	
	def end(self):
		self.active = False
		self.thread = None

	def p(self, parameter):
		with open(P_ROUTE, "r") as file:
			data = json.load(file)
			try:
				return data[parameter]
			except KeyError:
				print(f"\033[1mWARNING: [SimComs]\033[0m There is no parameter called \033[1m{parameter}\033[0m")
				return None