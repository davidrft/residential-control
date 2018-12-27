/*- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   - - - - - - PROJETO FINAL - MICROCOMPUTADORES: CASA INTELIGENTE - - - - - - - - - - - - - - - - - -
   - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   -
   -  ALUNOS ENVOLVIDOS:
   -  => AFONSO DE SÁ DELGADO NETO
   -  => DAVID RIFF DE FRANÇA TENÓRIO
   -  => DIEGO MAIA HAMILTON
   -  => EWELIM DAYANE DE SOUZA BARROS
   -
   -  VERSÃO: 1.0
   -  DATA: 27/12/2018
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  -                         DESCRIÇÃO DO ARQUIVO
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  -
  - O PROJETO APRESENTA UMA SOLUÇÃO DE UM SISTEMA EMBARCADO INTEGRADO A UMA INTERFACE VISUAL PARA
  - CONTROLE RESIDENCIAL AUTOMÁTICO OU REMOTO. O CONTROLE INCLUI: MOTOR DO PORTÃO DA GARAGEM, LUZES EM
  - DOIS AMBIENTES E AR-CONDICIONADO. NO DESENVOLVIMENTO, FOI UTILIZADO O MICROCONTROLADOR ATMEGA328P E
  - A PLATAFORMA ARDUINO, ALÉM DE SIMULAÇÕES NO PROTEUS E O DESENVOLVIMENTO DE UMA INTERFACE EM PYTHON,
  - CULMINANDO NUM PROTÓTIPO EM HARDWARE FÍSICO.
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
*/




#include <MsTimer2.h>

#define insideLight 13                 //pino da luz interna
#define outsideLight 12                //pino da luz externa
#define airConditioner 11              //pino do ar condicionado
#define buzzer 10                      //pino da buzina
#define motor 9                        //pino do motor
#define dirA 8                         //pino de controle ponte H
#define dirB 7                         //pino de controle ponte H
#define onOffLed 5                     //LED partida
#define startButton 4                  //pino de partida
#define insidePresenceSensor 3         //pino do sensor de presença interno
#define outsidePresenceSensor 2        //pino do sensor de presença externo
#define lumSensorIn A1                 //pino do sensor de luminosidade interno
#define lumSensorOut A2                //pino do sensor de luminosidade externo
#define tempSensor A0                  //pino do sensor de temperatura

String temperature;                    //string de temperatura
bool receiveTemp = false;
bool on = false;
bool userControl = false;
bool started = false;
int lumThreshold = 50;
int tempThreshold = 50;
bool isMotorOn = false;
bool panic = false;
bool openGate = true;
bool insideLightState = false,
     outsideLightState = false,
     airConditionerState = false;
int oldBuzzerValue = 0;
void pToggle(int pin) {                //toggle no buzzer - pânico
  if (panic)
    analogWrite(pin, 230);
  else
    analogWrite(pin, oldBuzzerValue);
}
void callbackInsidePresence(void) {   //função de callback para interrupção de presença interna
  if (insideLightState) {
    digitalWrite(insideLight, HIGH);
  } else {
    digitalWrite(insideLight, LOW);
  }
}
void callbackOutsidePresence(void) {  //função de callback para interrupção de presença externa
  if (outsideLightState) {
    digitalWrite(outsideLightState, HIGH);
  } else {
    digitalWrite(outsideLightState, LOW);
  }
}
void toggle(int pin) {
  digitalWrite(pin, !digitalRead(pin));  //toggle de pino
}
void automaticControl(void) {                                  //controle automático do programa
  if (digitalRead(insidePresenceSensor) &&
      analogRead(lumSensorIn) < lumThreshold)
  {
    digitalWrite(insideLight, HIGH);
    insideLightState = true;
  }
  else
  {
    digitalWrite(insideLight, LOW);
    insideLightState = false;
  }

  if (digitalRead(outsidePresenceSensor) &&
      analogRead(lumSensorOut) < lumThreshold)
  {
    digitalWrite(outsideLight, HIGH);
    outsideLightState = true;
  }
  else
  {
    digitalWrite(outsideLight, LOW);
    outsideLightState = false;
  }

  if (analogRead(tempSensor) > tempThreshold)
  {
    digitalWrite(airConditioner, HIGH);
    airConditionerState = true;
  }
  else
  {
    digitalWrite(airConditioner, LOW);
    airConditionerState = false;
  }
}

void takeCommand(char in) {                          //receber comando da serial
  switch (in) {
    case 'U':                                        //controle do usuário
      userControl = !userControl;
      break;
    case 'Z':                                   // setar temperatura na forma Z123# , temperatura vai para 123
      receiveTemp = true;
      break;
    case 'I':                                       //acende ou apaga luz interna
      if (userControl) {
        toggle(insideLight);
        insideLightState = !insideLightState;
      }
      break;
    case 'O':                                       //acende ou apaga luz externa
      if (userControl) {
        toggle(outsideLight);
        outsideLightState = !outsideLightState;
      }
      break;
    case 'A':                                       //acende ou apaga ar
      if (userControl) {
        toggle(airConditioner);
        airConditionerState = !airConditionerState;
      }
      break;
    case 'P':                                       //pânico
      panic = !panic;
      pToggle(buzzer);
      break;
    case 'G':                                       //
      if (openGate) {
        digitalWrite(dirA, HIGH);
        digitalWrite(dirB, LOW);
      }
      else {
        digitalWrite(dirA, LOW);
        digitalWrite(dirB, HIGH);
      }
      openGate = !openGate;
      analogWrite(motor, 128);
      isMotorOn = true;
      MsTimer2::start();
      break;
    case 'T': {
        int temp = (float)analogRead(tempSensor) * 100.0 * 5.0 / 1023.0;
        Serial.println(temp);
      } break;
    case 'S':
      Serial.println(analogRead(lumSensorIn));
      break;
    case 's':
      Serial.println(analogRead(lumSensorOut));
      break;
    case 'R': {
        int temp = (float)analogRead(tempSensor) * 100.0 * 5.0 / 1023.0;
        Serial.print(temp);
        Serial.print(' ');
        Serial.print(insideLightState);
        Serial.print(' ');
        Serial.print(outsideLightState);
        Serial.print(' ');
        Serial.println(airConditionerState);
      }
      break;
    default:
      break;
  }
}
void takeTemp(char in) {                            //obter valor de temperatura
  if (receiveTemp) {
    if (in == '#') {
      receiveTemp = false;
      tempThreshold = (float)1023 * temperature.toInt() / (5.0 * 100.0);
      temperature = "";
    } else
      temperature += in;
  }
}

void controlBuzzer(void) {                            //controlar a buzina
  if (!panic) {
    analogWrite(buzzer, oldBuzzerValue);
    if (isMotorOn)
      oldBuzzerValue = 128;
    else if (digitalRead(outsidePresenceSensor))
      oldBuzzerValue = 64;
    else
      oldBuzzerValue = 0;
  }
}

void callback() {                                    //callback do timer
  if (started) {
    isMotorOn = false;
    analogWrite(motor, 0);
    MsTimer2::stop();
  }
}

void setup() {                                      //declaração de pinos e inicialização do serial e timer
  pinMode(insideLight, OUTPUT);
  pinMode(outsideLight, OUTPUT);
  pinMode(airConditioner, OUTPUT);
  pinMode(motor, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(onOffLed, OUTPUT);
  pinMode(onOffLed, OUTPUT);
  pinMode(dirA, OUTPUT);
  pinMode(dirB, OUTPUT);
  pinMode(startButton, INPUT);
  pinMode(insidePresenceSensor, INPUT);
  pinMode(outsidePresenceSensor, INPUT);
  digitalWrite(startButton, HIGH);
  digitalWrite(insidePresenceSensor, HIGH);
  digitalWrite(outsidePresenceSensor, HIGH);
  Serial.begin(9600);
  temperature.reserve(200);
  MsTimer2::set(1000, callback);  //1s period
  MsTimer2::start();
}

void loop() {                           //loop principal
  if (digitalRead(startButton)) {
    started = true;
    digitalWrite(onOffLed, HIGH);
  }
  if (started) {
    if (!userControl) automaticControl();
    controlBuzzer();
  }
}

void serialEvent() {                    //interrupção serial
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (started) {
      takeTemp(inChar);
      takeCommand(inChar);
    }
  }
}

void presenceEvent() {                  //interrupção de presença
  callbackInsidePresence();
  callbackOutsidePresence();

}
