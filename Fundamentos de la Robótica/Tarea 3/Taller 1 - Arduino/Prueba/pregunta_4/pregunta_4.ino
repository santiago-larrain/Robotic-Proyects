#include <DualVNH5019MotorShield.h>

#include "DualVNH5019MotorShield.h"

DualVNH5019MotorShield md;

int pinA = 19;
int valorPaso = 0;
int tiempoAnterior = 0;
int timepoActual;

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
  attachInterrupt(digitalPinToInterrupt(pinA), actualizarValor, CHANGE);
}

void loop()
{
  // Prender por 1 segundo la rueda 2 y apagar la 1
  if (millis()%2000 == 0){
      md.setM1Speed(0);
      md.setM2Speed(-400*3/11.7);
    }
  
  // Prender por 1 segundo la rueda 1 y apagar la 2
  if (millis()%2000 == 5){
      md.setM1Speed(0);
      md.setM2Speed(-400*3/11.7);
    }
  // Imprimir el valor del pin A en todo momento
  Serial.print("Valor paso pin A: ");
  Serial.println(valorPaso);
}

void actualizarValor(){
  // Leer el estado actual del pin A
  // Esta función se llama cada vez que cambia de valor
  int timepoActual = millis();
  int valorPaso = tiempoActual - tiempoAnterior;
  int tiempoAnterior = tiempoActual;
}
