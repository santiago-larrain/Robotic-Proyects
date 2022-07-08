import numpy as np
import cv2
import time
from PIL import ImageFont, ImageDraw, Image

color_HSV_test = {
	'blue': np.array([110, 190, 155]),
	'red': np.array([7, 220, 155]),
	'yellow': np.array([25, 170, 145]),
	'green': np.array([65, 180, 155]),
}
rango = np.array([10, 65, 100])
c1 = 'red'
c2 = 'blue'
c3 = 'yellow'

nCam = 0
cap = cv2.VideoCapture(nCam) #

def filtro(col, fram):
	return cv2.inRange(fram, color_HSV_test[col] - rango, color_HSV_test[col] + rango)

def alpha(sin, cos):
	if sin >= 0 and cos >= 0:
		return np.arcsin(sin)
	elif sin >= 0 and cos < 0:
		return np.pi - np.arccos(-cos)
	elif sin < 0 and cos < 0:
		return np.arccos(-cos) - np.pi
	elif sin < 0 and cos >= 0:
		return np.arcsin(sin)
	return 0
	
def mostrar(src, txt, ID):
	cv2.putText(src, str(txt), (10, 20*ID), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

cv2.namedWindow('Observador | Original') #
cv2.moveWindow('Observador | Original', 0, 100) #
cv2.namedWindow('Observador | Filtrado') #
cv2.moveWindow('Observador | Filtrado', 640, 100) #

while(True):
	ret, frame1 = cap.read() #
	
	frame2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

	COLOR1 = filtro(c1, frame2)
	COLOR2 = filtro(c2, frame2)
	COLOR3 = filtro(c3, frame2)

	# # Centro de bolas
	try:
		ret, thresh = cv2.threshold(COLOR1, 127, 255, 0)
		M1 = cv2.moments(thresh)
		cX1 = int(M1["m10"] / M1["m00"])
		cY1 = int(M1["m01"] / M1["m00"])
		cv2.circle(frame1, (cX1, cY1), 5, (255, 255, 255), -1)
		ret, thresh = cv2.threshold(COLOR2, 127, 255, 0)
		M2 = cv2.moments(thresh)
		cX2 = int(M2["m10"] / M2["m00"])
		cY2 = int(M2["m01"] / M2["m00"])
		cv2.circle(frame1, (cX2, cY2), 5, (255, 255, 255), -1)
		ret, thresh = cv2.threshold(COLOR3, 127, 255, 0)
		M3 = cv2.moments(thresh)
		cX3 = int(M3["m10"] / M3["m00"])
		cY3 = int(M3["m01"] / M3["m00"])
		cv2.circle(frame1, (cX3, cY3), 5, (255, 255, 255), -1)

		mask = cv2.bitwise_or(COLOR1, COLOR2)
		mask = cv2.bitwise_or(mask, COLOR3)

		frame_AND = cv2.bitwise_and(frame1, frame1, mask= mask)
		# Linea entre C1 y C2
		cv2.line(frame_AND, (cX1, cY1), (cX2, cY2), (255, 255, 255), 3)
		# Linea entre C1 y C3
		cv2.line(frame_AND, (cX1, cY1), (cX3, cY3), (255, 255, 255), 3)
	except ZeroDivisionError or NameError:
		cv2.imshow('Observador | Filtrado', frame1)
	
	## --- Matemáticas --- ##
	try:
		vector_C1_C2 = np.array([cX2-cX1, -(cY2-cY1)])
		vector_C1_C3 = np.array([cX3-cX1, -(cY3-cY1)])
		sin_alpha = np.cross(vector_C1_C2, vector_C1_C3) / (np.linalg.norm(vector_C1_C2)*np.linalg.norm(vector_C1_C3))
		cos_alpha = vector_C1_C2.dot(vector_C1_C3) / (np.linalg.norm(vector_C1_C2)*np.linalg.norm(vector_C1_C3))
		angle = np.degrees(alpha(sin_alpha, cos_alpha))
		mostrar(frame_AND, f"Angle: {round(angle, 1)} deg", 1)
		mostrar(frame_AND, f"Distance: {int(np.linalg.norm(vector_C1_C3))} pix", 2)
		dist = 9*np.linalg.norm(vector_C1_C3)/np.linalg.norm(vector_C1_C2)
		mostrar(frame_AND, f"Distance: {round(dist, 2)} cm", 3)
	except NameError:
		pass

	try:
		cv2.imshow('Observador | Filtrado', frame_AND)
		cv2.imshow('Observador | Original', frame1)
	except NameError:
		cv2.imshow('Observador | Filtrado', frame1)

	## --- Inputs --- ##
	if cv2.waitKey(1) & 0xFF == 27: #
		break

cap.release()
cv2.destroyAllWindows()	