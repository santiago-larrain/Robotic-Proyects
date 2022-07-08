#define PinA 21
#define PinB 20
#define PinC 19
#define PinD 18

volatile double pos1 = 0.0;
volatile double pos1_prev = 0.0;
volatile double pos2 = 0.0;
volatile double pos2_prev = 0.0;
float vel1, vel2;

unsigned long newtime = 0.0;
unsigned long time_ant;
int Period = 1000.0;  // 1ms
int Period_seg = 0.001;

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

void setup() {
  Serial.begin(115200);


  pinMode(PinA, INPUT);
  pinMode(PinB, INPUT);
  pinMode(PinC, INPUT);
  pinMode(PinD, INPUT);

  attachInterrupt(digitalPinToInterrupt(PinA), EncoderA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinB), EncoderB, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinC), EncoderC, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PinD), EncoderD, CHANGE);

}

void loop() {
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
    Serial.print(" : ");
    Serial.println(vel2);
  }
}
