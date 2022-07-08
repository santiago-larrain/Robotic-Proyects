#include <DualVNH5019MotorShield.h>

#include "DualVNH5019MotorShield.h"

unsigned long tiempo1;
unsigned long tiempo2;


DualVNH5019MotorShield md;

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
  tiempo1 = millis();
}

void loop()
{

  for (int i = 0; i <= 400; i++)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM1Speed(i);
    stopIfFault();
    delay(2);
  }
  
  for (int i = 400; i >= -400; i--)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM1Speed(i);
    stopIfFault();
    delay(2);
  }
  
  for (int i = -400; i <= 0; i++)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM1Speed(i);
    stopIfFault();
    delay(2);
  }

  for (int i = 0; i <= 400; i++)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM2Speed(i);
    stopIfFault();
    delay(2);
  }
  
  for (int i = 400; i >= -400; i--)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM2Speed(i);
    stopIfFault();
    delay(2);
  }
  
  for (int i = -400; i <= 0; i++)
  {
    if (millis()%100 == 0){
      float volt = i*11.7 / 400;
      Serial.print("Voltaje: ");
      Serial.print(volt);
      Serial.println("V");
    }
    md.setM2Speed(i);
    stopIfFault();
    delay(2);
  }
}
