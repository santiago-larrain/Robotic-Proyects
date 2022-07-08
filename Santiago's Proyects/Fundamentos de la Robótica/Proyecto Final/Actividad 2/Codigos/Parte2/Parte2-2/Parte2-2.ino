#include <DualVNH5019MotorShield.h>
DualVNH5019MotorShield md;

char msgEnd = ';';
bool newMsg = false;
String msg;
float vel1, vel2;

void setup(){
  Serial.begin(119500);
  md.init();
}

void loop(){
  msg = readBuff();
  if (newMsg){
    Serial.println(msg);
    int index = msg.indexOf("/");
    vel1 = msg.substring(0,index).toFloat();
    vel2 = msg.substring(index + 1, msg.length()).toFloat();
    newMsg = false;
    md.setM1Speed(rpm2motor(-vel1));
    md.setM2Speed(rpm2motor(vel2));
  }
}

String readBuff() {
  String buffArray;
  //int i = 0;

  while (Serial.available() > 0) { //Entro a este while mientras exista algo en el puerto serial
    char buff = Serial.read(); //Leo el byte entrante
    if (buff == msgEnd) {
      newMsg = true;
      break; //Si el byte entrante coincide con mi delimitador, me salgo del while
    } else {
      buffArray += buff; //Si no, agrego el byte a mi string para construir el mensaje
      //i += 1;
    }
    delay(10);
  }

  return buffArray;  //Retorno el mensaje
}

float rpm2motor(float rpm){
  return rpm/60 * 40;
}
