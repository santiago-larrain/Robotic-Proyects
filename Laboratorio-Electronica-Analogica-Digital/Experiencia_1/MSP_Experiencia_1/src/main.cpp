#include <Arduino.h>
#include <msp430f5529.h>

// Variables para almacenar voltajes de entrada
int mil1 = 0, mil1_prev = 0;
int cien1 = 0, cien1_prev = 0;
int diez1 = 0, diez1_prev = 0;
int uno1 = 0, uno1_prev = 0;
// Variables para almacenar voltajes reales
int mil2 = 0, mil2_prev = 0;
int cien2 = 0, cien2_prev = 0;
int diez2 = 0, diez2_prev = 0;
int uno2 = 0, uno2_prev = 0;

// Función que revisa si el valor cambio, lo envia y espera a que se envie.
int send(int current, int previous, int pos){
	if (current != previous){
		// Solo enviar cambios si hubieron cambios
		uint8_t bcdValue = (pos << 4) | current;
		Serial1.write(bcdValue);
		Serial1.flush();
	}
	return current;
}

void setup() {
	Serial.begin(9600);
	// pinMode(RED_LED, OUTPUT);
	// pinMode(GREEN_LED, OUTPUT);
}

void loop() {
	double digital_v_in = analogRead(A1);
	double analog_v_in = 330*(1 - digital_v_in / 4095);
	
	// Obtener valores enteros y voltaje real
	int analog_v_in_int = int(analog_v_in);
	int analog_v_real_int = int(analog_v_in * 70/33 + 300);  // Funcion lineal

	// Separar digitos
	// Voltaje de entrada
	int uno1 = ((analog_v_in_int % 1000) % 100) % 10;
	int diez1 = ((analog_v_in_int % 1000) % 100) / 10;
	int cien1 = (analog_v_in_int % 1000) / 100;
	int mil1 = analog_v_in_int / 1000;
	// Voltaje real
	int uno2 = ((analog_v_real_int % 1000) % 100) % 10;
	int diez2 = ((analog_v_real_int % 1000) % 100) / 10;
	int cien2 = (analog_v_real_int % 1000) / 100;
	int mil2 = analog_v_real_int / 1000;
	
	// Enviar valores
	int uno1_prev = send(uno1, uno1_prev, 0x0);
	int diez1_prev = send(diez1, diez1_prev, 0x1);
	int cien1_prev = send(cien1, cien1_prev, 0x2);
	int mil1_prev = send(mil1, mil1_prev, 0x3);
	int uno1_prev = send(uno1, uno1_prev, 0x4);
	int diez1_prev = send(diez1, diez1_prev, 0x5);
	int cien1_prev = send(cien1, cien1_prev, 0x6);
	int mil1_prev = send(mil1, mil1_prev, 0x7);

// 	// Prototipo de codigo P2
// 	if (digital_v_in <= 1024){
// 		digitalWrite(RED_LED,HIGH) //LED1 ON
// 		digitalWrite(GREEN_LED,LOW) //LED2 OFF
// 	}
// 	else if(digital_v_in <=3072){
// 		digitalWrite(RED_LED,LOW) //LED1 ON
// 		digitalWrite(GREEN_LED,LOW) //LED2 ON
// 	}
// 	else{
// 		digitalWrite(RED_LED,HIGH) //LED1 OFF
// 		digitalWrite(GREEN_LED,HIGH) //LED2 ON
// 	}

// /* 	if (Serial.available() > 0) {
// 		String incoming = Serial.readString();
// 		Serial.print("I recieved:");
// 		Serial.println(incoming);
// 	} */
}