#include <DFRobot_DHT11.h>
#define DHT11_PIN 2
DFRobot_DHT11 DHT;
int btnPin = 9;
int btnState = 0;
int prevBtnState = 0;
int ArduinoID = 1;

void setup() {
  Serial.begin(9600);
  pinMode(btnPin, INPUT);
}

void loop(){
  btnState = digitalRead(btnPin);
  if(btnState != prevBtnState){
    if(btnState == HIGH){
      DHT.read(DHT11_PIN);
      int t = DHT.temperature;
      int h = DHT.humidity;

      Serial.print(ArduinoID);
      Serial.print(",");
      Serial.print(t);
      Serial.print(",");
      Serial.println(h);
      delay(1000);
    }
  }
  prevBtnState = btnState;
}