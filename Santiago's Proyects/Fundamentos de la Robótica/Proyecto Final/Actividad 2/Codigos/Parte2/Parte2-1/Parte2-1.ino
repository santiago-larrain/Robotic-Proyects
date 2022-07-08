#include <DualVNH5019MotorShield.h>
DualVNH5019MotorShield md;



void setup(){
  Serial.begin(119500);
  md.init();
}

void loop(){
  float vel = 120;
  md.setM1Speed(rpm2motor(-vel));
  md.setM2Speed(rpm2motor(vel));
}

float rpm2motor(float rpm){
  return rpm/60 * 40;
}
