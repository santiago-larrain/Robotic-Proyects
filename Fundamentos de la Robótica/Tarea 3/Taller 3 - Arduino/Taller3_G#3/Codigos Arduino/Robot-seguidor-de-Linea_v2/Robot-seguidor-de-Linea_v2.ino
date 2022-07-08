#include <DualVNH5019MotorShield.h>
DualVNH5019MotorShield md;

#include <QTRSensors.h>

/*
 * --------------------------------
 * Código de ejemplo de la librería
 * ´QTRSensors´  >  ´QTRRCExample´
 * --------------------------------
 * ****** MODIFICADO POR ******
 * *****  Matías Moreno   *****
 * *****   Jaime Tagle    *****
 * ***** Santiago Larraín *****
 * --------------------------------
 * --- Versión 2.0 - 27/04/2022 ---
 * --------------------------------
 * Consideraciones:
 *    Se hacen unos arreglos a la actualización del sistema.
 *    Anteriormente se utilizaba un controlador que trabajaba a 100Hz
 *    (10 ms), pero el loop de arduino se actualizaba cada 250 ms,
 *    por lo que había un retraso entre la señal y la respuesta que
 *    generaba problemas en las curvas.
 * ----------  UPDATES  -----------
 * > Se arregla el problema de frecuencia de trabajo, dejándolo en 100Hz.
 * > Error determinado con curva Tan[diferencia %]. Es más intuitiva al elevar los errores hacia los extremos.
 * > En caso de que la curva Tan[] genere grandes cambios ante pequeños errores, utilizar la
 *   función ArcSin[] (asin()), la cual es lineal en un intervalo central mayor, pero en los extremos es más curva.
 * > Se agrega la constante "curva" que permite elegir la curva de error {0: Lineal, 1: Arcotangente, 2: Arcoseno}
 *   esta constante se determina en la línea 89.
 * --------------------------------
 */

// This example is designed for use with eight RC QTR sensors. These
// reflectance sensors should be connected to digital pins 3 to 10. The
// sensors' emitter control pin (CTRL or LEDON) can optionally be connected to
// digital pin 2, or you can leave it disconnected and remove the call to
// setEmitterPin().
//
// The setup phase of this example calibrates the sensors for ten seconds and
// turns on the Arduino's LED (usually on pin 13) while calibration is going
// on. During this phase, you should expose each reflectance sensor to the
// lightest and darkest readings they will encounter. For example, if you are
// making a line follower, you should slide the sensors across the line during
// the calibration phase so that each sensor can get a reading of how dark the
// line is and how light the ground is.  Improper calibration will result in
// poor readings.
//
// The main loop of the example reads the calibrated sensor values and uses
// them to estimate the position of a line. You can test this by taping a piece
// of 3/4" black electrical tape to a piece of white paper and sliding the
// sensor across it. It prints the sensor values to the serial monitor as
// numbers from 0 (maximum reflectance) to 1000 (minimum reflectance) followed
// by the estimated location of the line as a number from 0 to 5000. 1000 means
// the line is directly under sensor 1, 2000 means directly under sensor 2,
// etc. 0 means the line is directly under sensor 0 or was last seen by sensor
// 0 before being lost. 5000 means the line is directly under sensor 5 or was
// last seen by sensor 5 before being lost.

// Definir constantes
unsigned long time_ant = 0;
unsigned long newtime;
float power_max = 60.0;    // Relacionado a la velocidad máxima del auto

float motorout0;
float motorout1;
float motorout_prev0 = power_max;    // Establecer la velocidad del auto en condiciones normales (sin error)
float motorout_prev1 = power_max;

// Se definene los valores con el punto decimal debido a bugs en arduino al usar números negativos cuando no se utiliza el .0
float ref = 3500.0;    // Posición que se intenta alcanzar
// Con método provando, estas constantes permiten realizar un giro suave a una velocidad dada por power_max = 60
float kp = 1.0;        // Constante de proporcionalidad
float ki = 0.01;       // Constante de integración
float kd = 0.01;       // Constante de derivación
const int Period = 10000;   // 10 ms = 100Hz
float Periodo_seg = 0.01;   // 10 ms
float k0 = kp*(1 + ki*Periodo_seg + kd*Periodo_seg);
float k1 = -kp*(1 + 2*kd/Periodo_seg);
float k2 = kp*kd/Periodo_seg;
float error0 = 0.0;
float error1 = 0.0;
float error_prev0 = 0.0;
float error_prev1 = 0.0;
float error_pprev0 = 0.0;
float error_pprev1 = 0.0;
// ------------------

// Elegir curva a utilizar ---
const int curva = 0;       // 0: Lineal, 1: Tangente, 2: Arcoseno

QTRSensors qtr;

const uint8_t SensorCount = 8;
uint16_t sensorValues[SensorCount];


void setup()
{
  // Configurar MotorShield
  md.init();
  
  // configure the sensors
  qtr.setTypeRC();
  qtr.setSensorPins((const uint8_t[]){A8, A9, A10, A11, A12, A13, A14, A15}, SensorCount);   // Recordar que el sensor está conectado con estos pines
  qtr.setEmitterPin(7);

  delay(500);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH); // turn on Arduino's LED to indicate we are in calibration mode

  // 2.5 ms RC read timeout (default) * 10 reads per calibrate() call
  // = ~25 ms per calibrate() call.
  // Call calibrate() 400 times to make calibration take about 10 seconds.
  for (uint16_t i = 0; i < 400; i++)
  {
    qtr.calibrate();
  }
  digitalWrite(LED_BUILTIN, LOW); // turn off Arduino's LED to indicate we are through with calibration

  // print the calibration minimum values measured when emitters were on
  Serial.begin(9600);
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.minimum[i]);
    Serial.print(' ');
  }
  Serial.println();

  // print the calibration maximum values measured when emitters were on
  for (uint8_t i = 0; i < SensorCount; i++)
  {
    Serial.print(qtr.calibrationOn.maximum[i]);
    Serial.print(' ');
  }
  Serial.println();
  Serial.println();
  delay(1000);
}

void loop()
{
  // read calibrated sensor values and obtain a measure of the line position
  // from 0 to 5000 (for a white line, use readLineWhite() instead)
  uint16_t position = qtr.readLineBlack(sensorValues);

  // Algortimo seguidor de linea (Actualizar a una frecuencia de 100Hz)
  if ((micros() - time_ant) >= Period)
  {
    newtime = micros();
    // En cada periodo, se calcula el error de cada rueda y se pondera para trabajarlo en motorout
    // A fin de que el auto haga las curvas más rápido, una rueda acelera y la otra desacelera; por esto tienen errores de signos opuestos
    if (curva == 0){
      error0 = (ref - position)/ref*power_max;
      error1 = (position - ref)/ref*power_max;
    }
    // Se utiliza una curva más intuitiva que es lineal para pequeños errores, pero para errores mayores crece
    // Se utilizó la curva tangente para lograr este efecto más intuitivo
    // Argumento in [-1, 1] --> Tan[argumento] in [-1.55, 1.55] --> error in [-93.4, 93.4]
    else if (curva == 1){
      error0 = tan((ref - position)/ref)*power_max;
      error1 = tan((position - ref)/ref)*power_max;
    }
    // OBS: Si se nota un cambio muy grande ante pequeños errores, se puede utilizar la función ArcSin[arg] --> asin()
    // Esta curva es más lineal en el centro, pero con gran curvatura en los extremos.
    else if (curva == 2){
      error0 = asin((ref - position)/ref)*power_max;
      error1 = asin((position - ref)/ref)*power_max;
    }
    
    // Actualizar las velocidades de las ruedas
    motorout0 = motorout_prev0 + k0*error0 + k1*error_prev0 + k2*error_pprev0;
    motorout1 = motorout_prev1 + k0*error1 + k1*error_prev1 + k2*error_pprev1;

    // Debido a que la rueda M1 está invertida, su valor debe ser el opuesto al obtenido
    md.setM1Speed(-motorout0);
    md.setM2Speed(motorout1);

    // Actualizar variables previas
    time_ant = newtime;
    motorout_prev0 = motorout0;
    motorout_prev1 = motorout1;
    error_prev0 = error0;
    error_prev1 = error1;
    error_pprev0 = error_prev0;
    error_pprev1 = error_prev1;
    // --- Fin Controlador ---
    
    // print the sensor values as numbers from 0 to 1000, where 0 means maximum
    // reflectance and 1000 means minimum reflectance, followed by the line
    // position
    for (uint8_t i = 0; i < SensorCount; i++)
    {
      Serial.print(sensorValues[i]);
      Serial.print('\t');
    }
    // Visualizar comportamiento del controlador para revisar su correcto funcionamiento
    Serial.print(position);
    Serial.print('\t');
    Serial.print(motorout0);
    Serial.print('\t');
    Serial.println(error0);
  }
}
