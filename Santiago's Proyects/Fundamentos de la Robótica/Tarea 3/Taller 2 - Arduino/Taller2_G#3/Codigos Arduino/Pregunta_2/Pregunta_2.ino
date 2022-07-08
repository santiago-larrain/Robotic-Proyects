/*
 * -----------------------------
 * IRB2001 - 2021-2
 * Modulo: Control de Sistemas Roboticos
 * -----------------------------
 * Programa Base Talleres del Curso
 * -----------------------------
 * ****** MODIFICADO POR ******
 * *****  Matías Moreno   *****
 * *****   Jaime Tagle    *****
 * ***** Santiago Larraín *****
 * -----------------------------
 */

//-----------------------------------
// IMPORTAR librearias
#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;

// Definición de PINs
#define encoder0PinA  19
#define encoder0PinB  18
#define encoder1PinA  20
#define encoder1PinB  21

// Variables Tiempo
unsigned long time_ant = 0;
const int Period = 10000;   // 10 ms = 100Hz
float escalon = 0;
const float dt = Period *0.000001f;
float motorout0    = 0.0;
float motorout1    = 0.0;
float motorout_prev0    = 0.0;
float motorout_prev1    = 0.0;

// Variables de los Encoders y posicion
volatile long encoder0Pos = 0;
volatile long encoder1Pos = 0;
long newposition0;
long oldposition0 = 0;
long newposition1;
long oldposition1 = 0;
unsigned long newtime;
float vel0;
float vel1;

// Se definen las siguientes variables a utilizar
float ref = 60;     // Velocidad que se intenta alcanzar
float kp = 1;       // Constante de proporcionalidad
float ki = 0;       // Constante de integración         // ki = 1, permite que el controlador llegué el valor referido
float kd = 0;       // Constante de derivación
float Periodo_seg = Period*0.0000001;    // 100Hz --> T = 10000us = 0.010 segundos
// Constantes utilizadas para el controlador (ver línea 160)
float k0 = kp*(1 + ki*Periodo_seg + kd*Periodo_seg);
float k1 = -kp*(1 + 2*kd/Periodo_seg);
float k2 = kp*kd/Periodo_seg;
// Se definien errores para cada motor a fin de que cada una sea controlada independientemente
long error0;          // error0(k)    , para un instante k
long error1;          // error1(k)
long error_prev0;     // error0(k-1)
long error_prev1;     // error1(k-1)
long error_pprev0;    // error0(k-2)
long error_pprev1;    // error1(k-2)



//-----------------------------------
// CONFIGURANDO INTERRUPCIONES
void doEncoder0A()
{
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
    encoder0Pos++;
  } else {
    encoder0Pos--;
  }
}

void doEncoder0B()
{
  if (digitalRead(encoder0PinA) == digitalRead(encoder0PinB)) {
    encoder0Pos--;
  } else {
    encoder0Pos++;
  }
}

void doEncoder1A()
{
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    encoder1Pos++;
  } else {
    encoder1Pos--;
  }
}

void doEncoder1B()
{
  if (digitalRead(encoder1PinA) == digitalRead(encoder1PinB)) {
    encoder1Pos--;
  } else {
    encoder1Pos++;
  }
}


//-----------------------------------
// CONFIGURACION
void setup()
{
  // Configurar MotorShield
  md.init();

  // Configurar Encoders
  pinMode(encoder0PinA, INPUT);
  digitalWrite(encoder0PinA, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder0PinB, INPUT);
  digitalWrite(encoder0PinB, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder1PinA, INPUT);
  digitalWrite(encoder1PinA, HIGH);       // Incluir una resistencia de pullup en le entrada
  pinMode(encoder1PinB, INPUT);
  digitalWrite(encoder1PinB, HIGH);       // Incluir una resistencia de pullup en le entrada
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoder0A, CHANGE);  // encoder 0 PIN A
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoder0B, CHANGE);  // encoder 0 PIN B
  attachInterrupt(digitalPinToInterrupt(encoder1PinA), doEncoder1A, CHANGE);  // encoder 1 PIN A
  attachInterrupt(digitalPinToInterrupt(encoder1PinB), doEncoder1B, CHANGE);  // encoder 1 PIN B

  // Configurar Serial port
  Serial.begin(115200);           //Inicializar el puerto serial (Monitor Serial)
  Serial.println("start");
}

//-----------------------------------
// LOOP PRINCIPAL
void loop() {
  if ((micros() - time_ant) >= Period)
  {
    newtime = micros();
    
    // //-----------------------------------
    // // Ejemplo variable alterando cada 5 segundos
    // if ((newtime / 5000000) % 2)
    //  escalon = 100.0;
    // else
    //   escalon = 0.0
    //-----------------------------------
    // Actualizando Informacion de los encoders
    newposition0 = encoder0Pos;
    newposition1 = encoder1Pos;

    //-----------------------------------
    // Calculando Velocidad del motor
    float rpm = 31250;
    vel0 = (float)(newposition0 - oldposition0) * rpm / (newtime - time_ant); //RPM
    vel1 = (float)(newposition1 - oldposition1) * rpm / (newtime - time_ant); //RPM
    oldposition0 = newposition0;
    oldposition1 = newposition1;

    //-----------------------------------
    // Salida al Motor (modificar aquí para implementar control
    
    // ----- Controlador ----
    // Sabemos que a una entrada de 40 (md.setMXSpeed(40)), se obtienen ~60 RPM
    error0 = (ref - vel0)/60*40;
    error1 = (ref - vel1)/60*40;
    motorout0 = motorout_prev0 + k0*error0 + k1*error_prev0 + k2*error_pprev0;
    motorout1 = motorout_prev1 + k0*error1 + k1*error_prev1 + k2*error_pprev1;
    
    // Motor Voltage
    md.setM1Speed(motorout0);
    md.setM2Speed(motorout1);

    // Reportar datos
    Serial.print("$,");
    Serial.print(newtime);
    Serial.print(",");
    Serial.print(newposition0);
    Serial.print(",");
    Serial.print(newposition1);
    Serial.print(",");
    Serial.print(vel0);
    Serial.print(",");
    Serial.print(vel1);
    Serial.print(",");
    Serial.print(motorout0);
    Serial.print(",");
    Serial.print(motorout1);
    Serial.println(",");

    // Actualizar valores previos
    time_ant = newtime;
    motorout_prev0 = motorout0;
    motorout_prev1 = motorout1;
    error_prev0 = error0;
    error_prev1 = error1;
    error_pprev0 = error_prev0;
    error_pprev1 = error_prev1;
  }

}
