

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  attachInterrupt(pin, ISR, modo);
  // pin = ordinal. Usar mejor digitalPinToInterrupt(N°pin en placa)
  // ISR = Interrupt Service Routine. Función o método que se llama al hacer la interrupción
  // modo = En qué estado del pin se lanza la interrupción:
  //        {LOW: pin en estado bajo, 
  //         CHANGE: pin cambia de estado (alto <--> bajo),
  //         RISING: pin pasa de estado bajo a alto,
  //         FALLING: pin pasa de estado alto a bajo,
  //         *HIGH: pin en estado alto *Solo en algunas placas}
  detachInterrupt(pin);    // anula la configuración del pin
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(millis());  // Devuelve el tiempo que lleva encendido en ms
  Serial.println(micros());  // Devuelve el tiempo que lleva encendido en us
  delay(500);
}
