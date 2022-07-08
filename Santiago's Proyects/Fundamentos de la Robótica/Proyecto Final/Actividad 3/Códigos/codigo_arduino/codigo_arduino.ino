#include <DualVNH5019MotorShield.h>
DualVNH5019MotorShield md;
#include <QTRSensors.h>

#define PinA 21
#define PinB 20
#define PinC 19
#define PinD 18

volatile double pos1 = 0.0;
volatile double pos1_prev = 0.0;
volatile double pos2 = 0.0;
volatile double pos2_prev = 0.0;
float vel1, vel2;
float ref1, ref2;
const int limit = 230;

unsigned long newtime = 0.0;
unsigned long time_ant;
float Period = 10000.0;  // 10 ms
float Period_seg = 0.01;

char msgEnd = ';';
bool newMsg = false;
String msg;

float motorout_prev1 = 0.0;
float motorout_prev2 = 0.0;
float motorout1;
float motorout2;
float kp = 2.0;        // Constante de proporcionalidad
float ki = 1.6;       // Constante de integración
float kd = 0.002;       // Constante de derivación
float k0 = kp*(1 + ki*Period_seg + kd/Period_seg);
float k1 = -kp*(1 + 2*kd/Period_seg);
float k2 = kp*kd/Period_seg;
float error1;
float error2;
float error_prev1 = 0.0;
float error_prev2 = 0.0;
float error_pprev1 = 0.0;
float error_pprev2 = 0.0;


void setup(){
  Serial.begin(119500);
  Serial3.begin(38400);
  md.init();
  
  pinMode(PinA, INPUT);
  pinMode(PinB, INPUT);
  pinMode(PinC, INPUT);
  pinMode(PinD, INPUT);

  attachInterrupt(digitalPinToInterrupt(PinA), EncoderA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinB), EncoderB, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinC), EncoderC, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinD), EncoderD, CHANGE);
}

void loop(){
  msg = readBuff();
  if (newMsg){
    Serial.println(msg);
    int index = msg.indexOf(",");
    // Limitar según capacidad de los motores
    ref1 = min(max(msg.substring(0,index).toFloat(), -limit), limit);
    ref2 = min(max(msg.substring(index + 1, msg.length()).toFloat(), -limit), limit);
    newMsg = false;
  }
    
  if (micros() - newtime >= Period){
    newtime = micros();
    // Calculando Velocidad del motor
    float rpm = 31250;
    vel1 = (float)(pos1 - pos1_prev) * rpm / (newtime - time_ant); //RPM
    vel2 = (float)(pos2 - pos2_prev) * rpm / (newtime - time_ant); //RPM
    
    time_ant = newtime;
    pos1_prev = pos1;
    pos2_prev = pos2;
    
    Serial.print(vel1);
    Serial.print(",");
    Serial.print(ref1);
    Serial.print(",");
    Serial.print(vel2);
    Serial.print(",");
    Serial.println(ref2);

    md.setM1Speed(-PID2());
    md.setM2Speed(PID1());
  }
}

// ****************************************************
// ****************************************************
// ****************************************************
// ****************************************************
// ****************************************************

String readBuff() {
  String buffArray;
  //int i = 0;

  while (Serial3.available() > 0) { //Entro a este while mientras exista algo en el puerto serial
    char buff = Serial3.read(); //Leo el byte entrante
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

void EncoderA() {
  if (digitalRead(PinA) != digitalRead(PinB)) { //
    pos1 = pos1 + 1;
  }
  else { //reversa
    pos1 = pos1 - 1;
  }
}
void EncoderB() {
  if (digitalRead(PinA) == digitalRead(PinB)) { //
    pos1 = pos1 + 1;
  }
  else { //Reversa
    pos1 = pos1 - 1;
  }
}
void EncoderC() {
  if (digitalRead(PinC) != digitalRead(PinD)) { //
    pos2 = pos2 + 1;
  }
  else { //reversa
    pos2 = pos2 - 1;
  }
}
void EncoderD() {
  if (digitalRead(PinC) == digitalRead(PinD)) { //
    pos2 = pos2 + 1;
  }
  else { //Reversa
    pos2 = pos2 - 1;
  }
}

// Controlador PID
float PID1(){
    error1 = (ref1 - vel1);
    motorout1 = motorout_prev1 + k0*error1 + k1*error_prev1 + k2*error_pprev1;
    motorout_prev1 = motorout1;
    error_pprev1 = error_prev1;
    error_prev1 = error1;
    return motorout1;
}

float PID2(){
    error2 = (ref2 - vel2);
    motorout2 = motorout_prev2 + k0*error2 + k1*error_prev2 + k2*error_pprev2;
    motorout_prev2 = motorout2;
    error_pprev2 = error_prev2;
    error_prev2 = error2;
    return motorout2;
}
