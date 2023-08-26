#include <Arduino.h>
#include <msp430f5529.h>


void setup() {
	Serial.begin(9600);
	// pinMode(RED_LED, OUTPUT);
	// pinMode(GREEN_LED, OUTPUT);
}

void loop() {
	double digital_v_in = analogRead(A1);
	double analog_v_in = 330*(1 - digital_v_in / 4095);
	
	int analog_v_in_int = int(analog_v_in);

	int mil = analog_v_in_int / 1000;
	int cien = (analog_v_in_int % 1000) / 100;
	int diez = ((analog_v_in_int % 1000) % 100) / 10;
	int uno = ((analog_v_in_int % 1000) % 100) % 10;
	Serial.println(digital_v_in);
	//Serial1.write(6 + 1*pow(2,4));
	

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
