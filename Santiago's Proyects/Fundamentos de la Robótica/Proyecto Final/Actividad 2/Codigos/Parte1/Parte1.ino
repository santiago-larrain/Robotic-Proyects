char msgEnd = ';';
bool newMsg = false;
String msg;

void setup(){
  Serial.begin(119500);
}

void loop(){
  msg = readBuff();
  if (newMsg){
    Serial.println(msg);
    newMsg = false;
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
