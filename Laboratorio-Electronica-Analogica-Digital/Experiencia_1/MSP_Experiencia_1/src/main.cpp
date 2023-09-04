#include <Arduino.h>
#include <msp430f5529.h>

// Variables para almacenar voltajes de entrada
int mil1  = 0, mil1_prev  = 0;
int cien1 = 0, cien1_prev = 0;
int diez1 = 0, diez1_prev = 0;
int uno1  = 0, uno1_prev  = 0;
// Variables para almacenar voltajes reales
int mil2  = 0, mil2_prev  = 0;
int cien2 = 0, cien2_prev = 0;
int diez2 = 0, diez2_prev = 0;
int uno2  = 0, uno2_prev  = 0;

// Variables para enviar datos cada 1 segundo
//     1 envio por UART son 10 bits, por lo que se hacen 480 envios cada segundo a un baudrate = 4800.
//     Cada un segundo se vuelven a enviar todos los datos, hayan cambiado o no.
bool send_all = false;
int count = 0;
int max_count = 480;

// Función que revisa si el valor cambio, lo envia y espera a que se envie.
int send(int current, int previous, int pos){
	if (current != previous | send_all){
		// Solo enviar cambios si hubieron cambios
		uint8_t bcdValue = pos | current;
		Serial1.write(bcdValue);
		Serial1.flush();
		count += 1;
	}
	return current;
}

void setup() {
	Serial1.begin(4800);
	pinMode(RED_LED, OUTPUT);
	pinMode(GREEN_LED, OUTPUT);
}

void loop() {
	double digital_v_in = analogRead(A1);
	double analog_v_in  = 330*(1 - digital_v_in / 4095);
	
	// Obtener valores enteros y voltaje real
	int analog_v_in_int   = int(analog_v_in);
	int analog_v_real_int = int(analog_v_in * 70/33 + 300);  // Funcion lineal

	// Separar digitos
	// Voltaje de entrada
	uno1  = ((analog_v_in_int % 1000) % 100) % 10;
	diez1 = ((analog_v_in_int % 1000) % 100) / 10;
	cien1 = (analog_v_in_int % 1000) / 100;
	mil1  = analog_v_in_int / 1000;
	// Voltaje real
	uno2  = ((analog_v_real_int % 1000) % 100) % 10;
	diez2 = ((analog_v_real_int % 1000) % 100) / 10;
	cien2 = (analog_v_real_int % 1000) / 100;
	mil2  = analog_v_real_int / 1000;
	
	// Enviar valores
	uno1_prev  = send(uno1, uno1_prev, 0x00);
	diez1_prev = send(diez1, diez1_prev, 0x10);
	cien1_prev = send(cien1, cien1_prev, 0x20);
	mil1_prev  = send(mil1, mil1_prev, 0x30);
	uno2_prev  = send(uno2, uno2_prev, 0x40);
	diez2_prev = send(diez2, diez2_prev, 0x50);
	cien2_prev = send(cien2, cien2_prev, 0x60);
	mil2_prev  = send(mil2, mil2_prev, 0x70);

 	// Encender Leds según nivel de voltaje
	// Como hay que invertir la entrada, si está entre 0-25%, el voltaje real está en realidad en 75-100%
	// Luego, se encienden los LEDS en entradas bajas y apagan en entradas altas.
 	if (digital_v_in <= 1024){
 		digitalWrite(RED_LED,HIGH); //LED1 OFF
 		digitalWrite(GREEN_LED,HIGH); //LED2 OFF
 	}
 	else if(digital_v_in <=3072){
 		digitalWrite(RED_LED,LOW); //LED1 OFF
 		digitalWrite(GREEN_LED,HIGH); //LED2 ON
 	}
 	else{
 		digitalWrite(RED_LED,LOW); //LED1 ON
 		digitalWrite(GREEN_LED,LOW); //LED2 ON
 	}

	// Enviar todos los datos cada un segundo, a modo de refrescar
	// la FPGA en caso de que esta haya sido reiniciada.
	if (count >= max_count){
		count = 0;
		send_all = true;
	}
	else {
		send_all = false;
	}

}