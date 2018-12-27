#include <MsTimer2.h>

#define insideLight 13
#define outsideLight 12
#define airConditioner 11
#define motor 9
#define buzzer 10
#define onOffLed 8
#define startButton 7
#define insidePresenceSensor 6
#define outsidePresenceSensor 5
#define lumSensorIn A1
#define lumSensorOut A2
#define tempSensor A0
#define openOrClose 2

String temperature;
bool receiveTemp = false;
bool on = false;
bool userControl = false;
bool started = false;
int lumThreshold = 512;
int tempThreshold = 50;
bool isMotorOn = false;
bool panic = false;
bool openGate = true;
bool insideLightState = false,
     outsideLightState = false,
     airConditionerState = false;
int oldBuzzerValue = 0;
void pToggle(int pin) {
  if (panic)
    analogWrite(pin, 230);
  else
    analogWrite(pin, oldBuzzerValue);
}
void toggle(int pin) { digitalWrite(pin, !digitalRead(pin)); }
void automaticControl(void) {
  if (!digitalRead(insidePresenceSensor) &&
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

  if (!digitalRead(outsidePresenceSensor) &&
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

void takeCommand(char in) {
  switch (in) {
    case 'U':
      userControl = !userControl;
      break;
    case 'Z':  // setar temperatura na forma Z123# , temperatura vai para 123
      receiveTemp = true;
      break;
    case 'I':
      if (userControl){ 
        toggle(insideLight);
        insideLightState = !insideLightState;
      }
      break;
    case 'O':
      if (userControl){
        toggle(outsideLight);
        outsideLightState = !outsideLightState;
        }
      break;
    case 'A':
      if (userControl) {
        toggle(airConditioner);
        airConditionerState = !airConditionerState;
      }
      break;
    case 'P':
      panic = !panic;
      pToggle(buzzer);
      break;
    case 'G':
      if (openGate)
        digitalWrite(openOrClose, HIGH);
      else
        digitalWrite(openOrClose, LOW);
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
    case 'R':
      int temp = (float)analogRead(tempSensor) * 100.0 * 5.0 / 1023.0;
      Serial.print(temp);
      Serial.print(' ');
      Serial.print(insideLightState);
      Serial.print(' ');
      Serial.print(outsideLightState);
      Serial.print(' ');
      Serial.println(airConditionerState);
      break;
    default:
      break;
  }
}
void takeTemp(char in) {
  if (receiveTemp) {
    if (in == '#') {
      receiveTemp = false;
      tempThreshold = (float)1023 * temperature.toInt() / (5.0 * 100.0);
      temperature = "";
    } else
      temperature += in;
  }
}

void controlBuzzer(void) {
  if (!panic) {
    analogWrite(buzzer, oldBuzzerValue);
    if (isMotorOn)
      oldBuzzerValue = 128;
    else if (!digitalRead(outsidePresenceSensor))
      oldBuzzerValue = 64;
    else
      oldBuzzerValue = 0;
  }
}

void callback() {
  if (started) {
    isMotorOn = false;
    analogWrite(motor, 0);
    MsTimer2::stop();
  }
}

void setup() {
  pinMode(insideLight, OUTPUT);
  pinMode(outsideLight, OUTPUT);
  pinMode(airConditioner, OUTPUT);
  pinMode(motor, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(onOffLed, OUTPUT);
  pinMode(onOffLed, OUTPUT);
  pinMode(openOrClose, OUTPUT);
  pinMode(startButton, INPUT);
  pinMode(insidePresenceSensor, INPUT);
  pinMode(outsidePresenceSensor, INPUT);
  digitalWrite(startButton, HIGH);
  digitalWrite(insidePresenceSensor, HIGH);
  digitalWrite(outsidePresenceSensor, HIGH);
  Serial.begin(9600);
  temperature.reserve(200);
  MsTimer2::set(1000, callback);  // 500ms period
  MsTimer2::start();
}

void loop() {
  if (!digitalRead(startButton)) {
    started = true;
    digitalWrite(onOffLed, HIGH);
  }
  if (started) {
    if (!userControl) automaticControl();
    controlBuzzer();
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (started) {
      takeTemp(inChar);
      takeCommand(inChar);
    }
  }
}
