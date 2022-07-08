#include <DualVNH5019MotorShield.h>

#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;

//////////////

// ¡DISCLAIMER!

// En caso de querer conseguir el número de pasos del encoder
// (considerando los pasos como cantidad de periodos)
// esta pregunta se resuelve con el archivo:
// "pregunta_3.ino"


// En caso de querer conseguir el valor del paso en cada instante,
// entendido como el largo del periodo en segundos, se resuelve 
// con el archivo: 
// "pregunta_4.ino" (este)

// DISCLAIMER 2: Descargo de responsabilidad.
// Código experimental, no testeado. Córralo bajo su propio riesgo
// 

//////////////

const int pinA = 19;
volatile unsigned long valorPaso = 0;
volatile unsigned long tiempoAnterior = 0;
volatile unsigned long tiempoActual = 0;

void stopIfFault()
{
  if (md.getM1Fault())
  {
    Serial.println("M1 fault");
    while(1);
  }
  if (md.getM2Fault())
  {
    Serial.println("M2 fault");
    while(1);
  }
}

void setup()
{
  Serial.begin(115200);
  Serial.println("Dual VNH5019 Motor Shield");
  md.init();
  attachInterrupt(digitalPinToInterrupt(19), actualizarValor, RISING);
}

void loop()
{
  Serial.print("Valor paso: T = ");
  Serial.print(valorPaso);
  Serial.print(" us");
}

void actualizarValor(){
  tiempoActual = micros();
  valorPaso = tiempoActual - tiempoAnterior;
  tiempoAnterior = tiempoActual;
}
