import numpy as np
import time
import serial

# Test de fuego: Done
msgs = ["0,0;", "200,200;", "100,300;", "200,200;", "0,0;", "-150,-150;", "-300,100;", "200,200;", "0,0;"]*5
delta_time = 5
t_prev = 0
i = 0

# Función
# Mensaje que quiero enviar
def msgOn(i, t_prev):
	if (time.time() - t_prev) >= delta_time:
		t_prev = time.time()
		i += 1
	return msgs[i], i, t_prev

# seria.Serial nos permite abrir el puerto COM deseado	
ser = serial.Serial("COM8",baudrate = 38400,timeout = 1)
time.sleep(1)

while(True):
	# El Ambos mensajes que estan en formato Sring deben ser transformados en un arreglo de bytes mediante la funcion .encode
	msg, i, t_prev = msgOn(i, t_prev)
	msgencode = str.encode(msg) 
	# .write nos permite enviar el arreglo de bytes correspondientes a los mensajes
	ser.write(msgencode);
	time.sleep(0.25)
	
# Cerramos el puerto serial abierto una vez terminado el codigo
ser.close()
