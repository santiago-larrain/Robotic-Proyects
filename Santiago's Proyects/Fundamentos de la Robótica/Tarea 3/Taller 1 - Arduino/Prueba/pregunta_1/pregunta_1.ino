#include <DualVNH5019MotorShield.h>

#include "DualVNH5019MotorShield.h"

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
}

void loop()
{
  md.setM1Speed(0);
  md.setM2Speed(-400*3/11.7);
  delay(5000);
  
  md.setM1Speed(400*3/11.7);
  md.setM2Speed(0);
  delay(5000);
  
  
  
}
